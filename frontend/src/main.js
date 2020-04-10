// This is the main.js file. Import global CSS and scripts here.
// The Client API can be used here. Learn more: gridsome.org/docs/client-api

import axios from 'axios';
import VueAxios from 'vue-axios';
import DefaultLayout from '~/layouts/Default.vue';

export default function(Vue, { router, head, isClient }) {
	// Set default layout as a global component
	Vue.component('Layout', DefaultLayout);
	Vue.use(VueAxios, axios);
	Vue.config.productionTip = false;
}
