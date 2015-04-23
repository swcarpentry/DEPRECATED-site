---
---
var SWC = SWC || {};

SWC.maps = (function() {
  var maps = {};

  function MarkerPin(color) {
    var pin = new google.maps.MarkerImage(
      "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + color,
      new google.maps.Size(21, 34),
      new google.maps.Point(0,0),
      new google.maps.Point(10, 34));
    return pin;
  }

  function MarkerPinCluster(url, sizeX, sizeY) {
    var pin = new google.maps.MarkerImage(
    url,
    new google.maps.Size(sizeX,sizeY),
    new google.maps.Point(0,0),
    new google.maps.Point(10,34));
    return pin;
  }

  function set_info_window(map, marker, info_window, content) {
    google.maps.event.addListener(marker, 'click', function () {
      info_window.setContent(content);
      info_window.open(map, marker);
    });
  }

  function enableScrollwheel(map) {
    if(map) map.setOptions({ scrollwheel: true });
  }

  function disableScrollwheel(map) {
    if(map) map.setOptions({ scrollwheel: false });
  }

  function toggle_marker_visibility(marker) {
    if (marker.getVisible()) {
      marker.setVisible(false);
    } else {
      marker.setVisible(true);
    }
  }

  function toggle_markers_mc_visibility(markers, mc) {
    markers.forEach(toggle_marker_visibility);
    if (markers[0].visible) {
      mc.setMap(markers[0].getMap());
    }
    else {
      mc.setMap(null);
    }
  }

  function add_cluster_event_listeners(clusterer, map, info_window) {
    google.maps.event.addListener(clusterer, 'clusterclick', function(cluster) {
      info_window.setPosition(cluster.getCenter());
      var info_string = "<div class=\"info-window\">";
      var i=0;
      var markers = cluster.getMarkers();
      for (; i < markers.length; i++ )
      {
        info_string += markers[i].getTitle();
      }
        info_string += "</div>";
        // reset content so that scroll bar in new content will always be at
        // top of content
        info_window.setContent( "<div class=\"info-window\"></div>");
        info_window.setContent(info_string);
        info_window.open(map);
        // when the info window has a scroll bar, we want the mouse scroll wheel
        //   to scroll in the info window, NOT zoom the map.  Disable map zoom.
        disableScrollwheel(map);
    });
    // zooming changes our clusters completely.  The info window is no longer
    //  accurate.  Close it.  Make people pick a new cluster or marker.
    google.maps.event.addListener(map, 'zoom_changed', function(event){
        info_window.close();
    });
    // when the info window is closed, restore mousewheel zoom on the map
    google.maps.event.addListener(info_window, 'closeclick', function(){
      enableScrollwheel(map);
    });
  };


  maps.upcoming = function() {
    var mapOptions = {
      zoom: 2,
      center: new google.maps.LatLng(25,8),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    },
    info_window   = new google.maps.InfoWindow({}),
    map           = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

    // Go over all the upcoming camps and create pins in the map
    {% for workshop in site.workshops %}
      {% if workshop.latlng and workshop.startdate >= site.today %}
        var marker = new google.maps.Marker({
          position: new google.maps.LatLng({{workshop.latlng}}),
          map: map,
          title: "{{workshop.venue}}, {{workshop.humandate}}",
          //icon: openPin,
          visible: true,
        });
        var info_string = "<div class=\"info-window\">" +
          "<h5><a href=\"{% if workshop.url %}{{workshop.url}}{% else %}{{page.root}}/{{workshop.path}}{% endif %}\">{{workshop.venue}}</a></h5>" +
          "<h6><a href=\"{{page.root}}/{{workshop.path}}\">{{workshop.humandate}}</a></h6>" +
          "</div>";
        set_info_window(map, marker, info_window, info_string);
      {% endif %}
    {% endfor %}
  }

  maps.previous = function() {
    var mapOptions = {
      zoom: 2,
      center: new google.maps.LatLng(25,8),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    },
    map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    var markers = [];
    var info_window = new google.maps.InfoWindow();
    // Go over all the previous camps and create pins in the map
    {% for workshop in site.workshops reversed %}
      {% if workshop.latlng and workshop.startdate < site.today %}
        var marker = new google.maps.Marker({
          position: new google.maps.LatLng({{workshop.latlng}}),
          map: map,
          title: "<h5><a href=\"{% if workshop.url %}{{workshop.url}}{% else %}{{page.root}}/{{workshop.path}}{% endif %}\">{{workshop.venue}}</a></h5>" +
          "<h6><a href=\"{{page.root}}/{{workshop.path}}\">{{workshop.humandate}}</a></h6>",
          //icon: openPin,
          visible: true,
        });
        var info_string = "<div class=\"info-window\">" +
          "<h5><a href=\"{% if workshop.url %}{{workshop.url}}{% else %}{{page.root}}/{{workshop.path}}{% endif %}\">{{workshop.venue}}</a></h5>" +
          "<h6><a href=\"{{page.root}}/{{workshop.path}}\">{{workshop.humandate}}</a></h6>" +
          "</div>";
        set_info_window(map, marker, info_window, info_string);
        markers.push(marker); // For clustering
      {% endif %}
    {% endfor %}

    var mcOptions = {
          zoomOnClick: false,
          maxZoom: null,
          gridSize: 25,
          minimumClusterSize: 2
        }
    var mc = new MarkerClusterer(map, markers, mcOptions);
    add_cluster_event_listeners(mc, map, info_window);
  }

  maps.instructors = function() {
    var mapOptions = {
      zoom: 2,
      center: new google.maps.LatLng(25,8),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    },
    info_window   = new google.maps.InfoWindow({}),
    map           = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
    var markers = [];
    var mcOptions = {
          maxZoom: null,
          gridSize: 25,
          minimumClusterSize: 1
        }
    // Go over all airports to read instructor location
    {% for airport in site.airports %}
        {% for i in (1..{{airport.count}}) %}
            var marker = new google.maps.Marker({
              position: new google.maps.LatLng({{airport.latlng}}),
              map: map,
              visible: false // marker not shown directly, just clustered
	        });
    	    markers.push(marker); // For clustering
		{% endfor %}
	{% endfor %}
    var mc = new MarkerClusterer(map,markers,mcOptions);
  }

  return maps;
})();
