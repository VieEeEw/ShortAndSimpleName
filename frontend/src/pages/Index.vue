<template>
	<Layout>
        <md-card>
            <md-card-header>
                <div class="md-title">Find Classes</div>
            </md-card-header>
            <md-divider></md-divider>
            <md-card-content>
                <md-tabs class="md-transparent" md-alignment="fixed" md-active-tab="tab-subject">
                  <md-tab id="tab-subject" md-label="Subject">
                    <form>
                        <md-field>
                            <label>Subject...</label>
                            <md-input type="text" v-model="subjectForm.name" required />
                        </md-field>
                    </form>
                  </md-tab>
                  <md-tab id="tab-location" md-label="Location">
                      <form>
                        <md-field>
                            <label>Location...</label>
                            <md-input type="text" v-model="locationForm.name" required />
                        </md-field>
                    </form>
                  </md-tab>
                  <md-tab id="tab-time" md-label="Time">
                      <form>
                        <md-field>
                            <label>Time...</label>
                            <md-input type="text" v-model="timeForm.name" required />
                        </md-field>
                    </form>
                  </md-tab>
            </md-tabs>
            </md-card-content>
            
            <md-divider></md-divider>
            <md-card-header>
                <div class="md-title">Applied Filters</div>
            </md-card-header>
            <md-divider></md-divider>
            <md-card-content>
            </md-card-content>
        </md-card>
	</Layout>
</template>

<script>
const initialState = {
  isLoggedIn: false,
  currentUser: {
    name: "",
    net_id: ""
  },
  loginForm: {
    net_id: "",
    password: ""
  },
  registerForm: {
    net_id: "",
    name: "",
    password: ""
  }
};

export default {
  name: "Home",
  data() {
    return {
        subjectForm: { ...initialState.subjectForm },
        locationForm: { ...initialState.locationForm },
        timeForm: { ...initialState.timeForm }
    };
  },
  methods: {
    
  }
};
</script>

<style>

</style>
