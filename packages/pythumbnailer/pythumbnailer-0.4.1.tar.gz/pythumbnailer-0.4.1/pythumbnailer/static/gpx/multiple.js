// Part of pythumbnailer: https://gitlab.com/somini/pythumbnailer/
var TILE_DATA = {
	'OpenTopoMap': {
		url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
		options: {
			attribution: 'Map Data: &copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map Style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
		},
	},
	'OpenStreetMap': {
		url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
		options: {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
		},
	},
	'OpenTopoMap @ Valentim': {
		url: 'https://map.valentim.org/otmpt/{z}/{x}/{y}.png',
		options: {
			attribution: 'Mosaico: <a href="http://valentim.org">valentim.org</a> | Dados: Contribuidores do <a href="https://www.openstreetmap.org/about">OpenStreetMap</a>, <a href="https://land.copernicus.eu/imagery-in-situ/eu-dem">Copernicus</a>, <a href="http://www.hidrografico.pt/op/33">Instituto Hidrográfico</a> | Estilo: <a href="https://github.com/der-stefan/OpenTopoMap">OpenTopoMap</a>, &copy; <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>',
		},
	},
	'World Imagery': {
		url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
		options: {
			attribution: 'Powered by <a href="https://www.esri.com">Esri</a>',
		},
	},
	'National Geographic': {
		url: 'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
		options: {
			attribution: 'National Geographic, DeLorme, HERE, UNEP-WCMC, USGS, NASA, ESA, METI, NRCAN, GEBCO, NOAA, increment P Corp. | Powered by <a href="https://www.esri.com">Esri</a>',
		},
	},
}
var COLORS = [
	'red',
	'orange',
	'brown', // 'yellow',
	'green',
	'blue',
	'purple',
	'#787132',
	'#d4cdc4',
	'#c8a98c',
	'#d5a129',
	'#9b4e23',
	'#c8beb9',
	'#a81817',
	'#344d2f',
	'#3e0610',
]

// Default Track Index
var default_track = Number(document.getElementById('map').dataset['defaultTrack']) || 0
// Default Tile Data
var default_tile = document.getElementById('map').dataset['defaultTile'] || 'OpenTopoMap'

// ---

function showTrackIndex(index) {
	var track = tracks[index]
	console.log(`Show #${index}`)
	// Show on map
	track.addTo(map)
	// Show data on the elevation widget
	// TODO: Don't re-load the data, Performance!!!
	controlElevation.clear()
	track.lines.forEach((line) => {
		controlElevation.addData(line, track)
	})
	// Jump to view
	map.fitBounds(track.getBounds())
}

function clickLayer(e) {
	var index = Number(e.target.dataset['tid'])
	showTrackIndex(index)
	e.stopPropagation()
	return false
}

function wireTrackLinks() { // Idempotent
	var tids = document.querySelectorAll('a.tid')
	// console.log('TrackID:', tids)
	tids.forEach((node) => {
		node.onclick = clickLayer
	})
}


// ---

var static_location = document.getElementById('static-location').href;

// Base Layers
// https://leafletjs.com/reference-1.3.2.html#tilelayer
var baseLayers = {}
Object.keys(TILE_DATA).forEach((key) => {
	var tile = TILE_DATA[key]
	baseLayers[key] = L.tileLayer(tile.url, tile.options)
})

var map = L.map('map', {
	zoomControl: false,
	layers: [baseLayers[default_tile]],
})

// Zoom
// https://leafletjs.com/reference-1.3.2.html#control-zoom
var controlZoom = new L.Control.Zoom({
	position: 'topleft',
})
controlZoom.addTo(map)

// Layers Selector
var controlLayer = L.control.layers(baseLayers, null, {
	position: 'topright', // position: 'topleft',
	hideSingleBase: false,
	collapsed: false, // collapsed: true,
})
controlLayer.addTo(map)

// Track Elevation Viewer
var controlElevation = L.control.elevation({
	theme: 'steelblue-theme',
	summary: 'description',
	detached: false,
	autohide: true,
	collapsed: false,
	legend: false,
	position: 'bottomleft',
	interpolation: "curveLinear", // Default
	// Slope
	slope: true,
	sInterpolation: "curveMonotoneX", // Smooth the slope
	// More than 100% slope deltas (for each side) is probably an error
	sDeltaMax: 100,
	// TODO: Make this configurable from the outside?
})
controlElevation.addTo(map)

// Tracks
var tracks = []
var track_promises = []
// TODO: Move this to a generated JSON file and load it using `fetch`
for (let track_name in GLOBAL_DATA['tracks']) {
	var track_url = GLOBAL_DATA['tracks'][track_name]
	var track = new L.GPX(track_url, {
		async: true,
		marker_options: { // The markers are a bit ugly...
			startIconUrl: false, // `${static_location}/lib/images/default-pin.start.png`,
			endIconUrl: false,   // `${static_location}/lib/images/default-pin.end.png',
			shadowUrl: false,    // `${static_location}/lib/images/pin-shadow.png',
			wptIconUrls: {
				'': false,   // `${static_location}/lib/images/default-pin.waypoint.png',
			},
		},
	});
	let track_idx = tracks.length
	tracks.push(track)
	track_promises.push(new Promise((resolve, reject) => {
		track.once('loaded', function(e) {
			console.log(`Loaded #${track_idx}: ${track_name}`)
			var track = e.target
			track.NAME = track_name
			track.INDEX = track_idx
			track.addTo(map)
			resolve()
		})
		track.lines = []
		track.on('addline', (e) => {
			e.target.lines.push(e.line)
		})
	}))
}

// Get the track index from the window hash
var track_hash = window.location.hash.substring(1)
var track_number = Number(track_hash)
if (track_hash !== "" && track_number !== NaN) {
	default_track = track_number
}
tracks[default_track].once('loaded', (e) => {
	showTrackIndex(default_track)
})

Promise.all(track_promises).then(() => {
	console.log('All Tracks Loaded')
	// Setup the Overlay list
	tracks.forEach((track) => {
		var track_idx = track.INDEX
		var track_color = COLORS[track_idx % COLORS.length]
		track.setStyle({
			weight: 5,
			color: track_color,
		})
		controlLayer.addOverlay(track, `Track "<a href="#${track_idx}" class="tid" style="color:${track_color}" data-tid="${track_idx}">${track.NAME}</a>"`)
	})
	wireTrackLinks()
})
map.on('overlayadd overlayremove', (e) => {
	// Re-Wire Track Links, sometimes the events disappear
	wireTrackLinks()
	return true
})
