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

  maps.upcoming = function() {
    var mapOptions = {
      zoom: 2,
      center: new google.maps.LatLng(25,8),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    },
    info_window   = new google.maps.InfoWindow({}),
    map           = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

    // Go over all the upcoming camps and create pins in the map
    {% for bootcamp in site.bootcamps %}
      {% if bootcamp.latlng and bootcamp.startdate >= site.today %}
        var marker = new google.maps.Marker({
          position: new google.maps.LatLng({{bootcamp.latlng}}),
          map: map,
          title: "{{bootcamp.venue}}, {{bootcamp.humandate}}",
          //icon: openPin,
          visible: true,
        });

        var info_string = '<div class="info-window">' +
          '<h5><a href="{% if bootcamp.url %}{{bootcamp.url}}{% else %}{{page.root}}/{{bootcamp.path}}{% endif %}">{{bootcamp.venue|replace: '\'','\\\''}}</a></h5>' +
          '<h6><a href="{{page.root}}/{{bootcamp.path}}">{{bootcamp.humandate}}</a></h6>' +
          '</div>';

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
    info_window   = new google.maps.InfoWindow({}),
    map           = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

    // Go over all the upcoming camps and create pins in the map
    {% for bootcamp in site.bootcamps %}
      {% if bootcamp.latlng and bootcamp.startdate < site.today %}
        var marker = new google.maps.Marker({
          position: new google.maps.LatLng({{bootcamp.latlng}}),
          map: map,
          title: "{{bootcamp.venue}}, {{bootcamp.humandate}}",
          //icon: openPin,
          visible: true,
        });

        var info_string = '<div class="info-window">' +
          '<h5><a href="{% if bootcamp.url %}{{bootcamp.url}}{% else %}{{page.root}}/{{bootcamp.path}}{% endif %}">{{bootcamp.venue|replace: '\'','\\\''}}</a></h5>' +
          '<h6><a href="{{page.root}}/{{bootcamp.path}}">{{bootcamp.humandate}}</a></h6>' +
          '</div>';

            set_info_window(map, marker, info_window, info_string);
      {% endif %}
    {% endfor %}
  }

  return maps;
})();
