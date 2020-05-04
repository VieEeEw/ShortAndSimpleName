// This is the main.js file. Import global CSS and scripts here.
// The Client API can be used here. Learn more: gridsome.org/docs/client-api

import axios from 'axios';
import VueAxios from 'vue-axios';
import DefaultLayout from '~/layouts/Default.vue';

import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';

import * as VueGoogleMaps from 'vue2-google-maps';

export default function(Vue, { router, head, isClient }) {
	// Set default layout as a global component
	Vue.component('Layout', DefaultLayout);
	Vue.use(VueAxios, axios);
	Vue.use(VueMaterial);
	head.link.push({
		rel: 'stylesheet',
		href: '//fonts.googleapis.com/css?family=Roboto:400,500,700,400italic|Material+Icons',
	});

	Vue.use(VueGoogleMaps, {
		load: {
			key: process.env.GRIDSOME_GOOGLE_MAPS_KEY,
			libraries: 'places',
		},
		installComponents: true,
	});

	Vue.config.productionTip = false;
}
