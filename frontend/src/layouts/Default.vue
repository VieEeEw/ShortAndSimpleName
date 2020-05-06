<template>
  <div style="height: 100%; width:100%;">
    <div :class="{ 'layout-inactive': menuClosed }" class="layout">
      <div :class="{ 'main-drawer-inactive': menuClosed }" class="main-drawer">
        <i
          @click="drawerToggle"
          :class="{ 'main-drawer-toggle-inactive': menuClosed }"
          class="main-drawer-toggle material-icons"
        />
        <div style="box-sizing:border-box; padding:10px 30px; margin-top:15px;">
          <slot />
        </div>
        <div v-if="isMobile" class="user-profile-docker">
          <UserProfile />
        </div>
      </div>
      <GmapMap :center="mapOpts.center" :markers="markers" class="map" :options="mapOpts">
        <GmapMarker :key="index" :position="m.position" v-for="(m, index) in markers" />
        <GmapPolyline
          :options="{
          strokeColor: '#FF0000',
          strokeOpacity: 0.5,
          }"
          :key="index"
          :path="p"
          v-for="(p, index) in paths"
        />
      </GmapMap>
    </div>
    <div v-if="!isMobile" class="user-profile-overlay">
      <UserProfile />
    </div>
  </div>
</template>

<static-query>
query {
  metadata {
    siteName
  }
}
</static-query>

<style>
html,
body {
  font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.5;
  width: 100%;
  height: 100%;
}

.layout {
  display: grid;
  width: 100%;
  height: 100%;
  grid-template: "drawer map" 1fr / 400px 1fr;
}

.layout-inactive {
  grid-template: "drawer map" 1fr/ 60px 1fr;
}

.main-drawer {
  position: relative;
  z-index: 9;
  display: block;
  overflow: hidden;
  -webkit-box-shadow: 0px 0px 35px 5px rgba(0, 0, 0, 0.48);
  box-shadow: 0px 0px 45px 0px rgba(0, 0, 0, 0.3);
}

.main-drawer-inactive::before {
  content: "";
  position: absolute;
  z-index: 99;
  width: 100%;
  height: 100%;
  background-color: white;
}

.main-drawer-toggle {
  position: absolute;
  top: 10px;
  right: 20px;
  width: 35px;
  height: 35px;
  cursor: pointer;
  user-select: none;
  font-size: 35px !important;
  color: rgba(0, 0, 0, 0.25);
}

.main-drawer-toggle::before {
  position: absolute;
  z-index: 999;
  width: 100%;
  height: 100%;
  left: 17px;
  content: "arrow_back_ios";
}

.main-drawer-toggle-inactive::before {
  content: "arrow_forward_ios";
  left: 9px;
}

.map {
  position: relative;
  display: block;
  z-index: 0;
}

.user-profile-overlay {
  position: absolute;
  box-sizing: border-box;
  padding: 15px;
  z-index: 999;
  right: 15px;
  top: 15px;
  display: block;
  width: 300px;
  border-radius: 15px;
  overflow: hidden;
  background-color: white;
  -webkit-box-shadow: 0px 0px 35px 5px rgba(0, 0, 0, 0.48);
  box-shadow: 0px 0px 45px 0px rgba(0, 0, 0, 0.3);
}
</style>

<script>
import UserProfile from "~/components/UserProfile.vue";
const isMobile = window.innerWidth < 800;

export default {
  props: ["markers", "paths"],
  components: {
    UserProfile
  },
  data() {
    return {
      isMobile,
      menuClosed: isMobile,
      mapOpts: {
        zoom: 17,
        center: {
          lat: 40.108248,
          lng: -88.227261
        },
        mapTypeId: "roadmap",
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        disableDefaultUI: false,
        styles: [
          {
            featureType: "administrative.neighborhood",
            stylers: [{ visibility: "off" }]
          },
          { featureType: "poi.attraction", stylers: [{ visibility: "off" }] },
          { featureType: "poi.business", stylers: [{ visibility: "off" }] },
          { featureType: "poi.government", stylers: [{ visibility: "off" }] },
          { featureType: "poi.medical", stylers: [{ visibility: "off" }] },
          {
            featureType: "poi.sports_complex",
            stylers: [{ visibility: "off" }]
          },
          { featureType: "poi.school", stylers: [{ visibility: "off" }] },
          {
            featureType: "poi.place_of_worship",
            stylers: [{ visibility: "off" }]
          },
          {
            featureType: "road.highway",
            elementType: "labels",
            stylers: [{ visibility: "off" }]
          }
        ]
      }
    };
  },
  methods: {
    drawerToggle(e) {
      e.preventDefault();
      this.menuClosed = !this.menuClosed;
    }
  }
};
</script>
