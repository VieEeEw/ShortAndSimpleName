<template>
  <div class="profile-container">
    <div>
      <md-avatar v-if="isLoggedIn" class="profile-icon md-avatar-icon">{{currentUser.name[0]}}</md-avatar>
    </div>
    <div class="profile-details">
      <div v-if="isLoggedIn" class="user-details-grid">
        <span></span>
        <span style="font-size:17px; font-weight:500; color:#333">{{currentUser.name}}</span>
        <span
          style="font-size:12px; font-weight:100; color:#aaa"
        >{{' '+ currentUser.net_id+'@illinois.edu'}}</span>
      </div>
      <div v-if="!isLoggedIn">
        <md-tabs md-alignment="centered" md-active-tab="tab-login">
          <md-tab id="tab-login" md-label="Login">
            <form @submit="loginUser">
              <md-field>
                <label>Net ID</label>
                <md-input type="text" v-model="loginForm.net_id" required />
              </md-field>
              <md-field>
                <label>Password</label>
                <md-input type="password" v-model="loginForm.password" required />
              </md-field>
              <div style="position:relative; width:100%; height:30px;">
                <md-button
                  style="position:absolute; right:0;"
                  class="md-primary md-raised"
                  type="submit"
                >Sign in</md-button>
              </div>
            </form>
          </md-tab>
          <md-tab class="md-primary" id="tab-register" md-label="Register">
            <form @submit="registerUser">
              <md-field>
                <label>Name</label>
                <md-input type="text" v-model="registerForm.name" required />
              </md-field>
              <md-field>
                <label>Net ID</label>
                <md-input type="text" v-model="registerForm.net_id" required />
              </md-field>
              <md-field>
                <label>Password</label>
                <md-input type="password" v-model="registerForm.password" required />
              </md-field>
              <div style="position:relative; width:100%; height:30px;">
                <md-button
                  style="position:absolute; right:0;"
                  class="md-primary md-raised"
                  type="submit"
                >Register</md-button>
              </div>
            </form>
          </md-tab>
        </md-tabs>
      </div>
    </div>
    <div class="profile-buttons"></div>
    <div class="profile-signout">
      <div v-if="isLoggedIn" style="position: relative; height:30px;">
        <div class="center">
          <md-button @click="logoutUser" style="border: 1px solid rgba(0,0,0,0.05);">Sign out</md-button>
        </div>
      </div>
    </div>
  </div>
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
  name: "UserProfile",
  data() {
    return {
      isLoggedIn: initialState.isLoggedIn,
      currentUser: { ...initialState.currentUser },
      loginForm: { ...initialState.loginForm },
      registerForm: { ...initialState.registerForm }
    };
  },
  methods: {
    logoutUser() {
      this.isLoggedIn = false;
      this.currentUser = { ...initialState.currentUser };
      this.loginForm = { ...initialState.loginForm };
      this.registerForm = { ...initialState.registerForm };
    },
    async loginUser(e) {
      e.preventDefault();
      try {
        // Try to POST the login request 🤞
        const { data } = await this.axios.post(
          "http://localhost:5000/auth/login",
          this.loginForm
        );
        this.currentUser = {
          name: "John Appleseed",
          net_id: this.loginForm.net_id
        };
        this.isLoggedIn = true;
      } catch (err) {
        // Oops, something went wrong. Tell the user 😫
        alert(err.response.data.error);
      }
    },
    async registerUser(e) {
      e.preventDefault();
      try {
        // Try to POST the new user 🤞
        const { data } = await this.axios.post(
          "http://localhost:5000/auth/register",
          this.registerForm
        );
        this.currentUser = {
          name: this.registerForm.name,
          net_id: this.registerForm.net_id
        };
        this.isLoggedIn = true;
      } catch (err) {
        // Oops, something went wrong. Tell the user 😫
        alert(err.response.data.error);
      }
    }
  }
};
</script>

<style>
.center {
  position: absolute;
  display: block;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.profile-container {
  position: relative;
  display: grid;
  height: 100%;
  width: 100%;
  grid-gap: 15px;
  grid-template: "icon details details" auto "buttons buttons signout" auto / auto 1fr auto;
}
.profile-icon {
  grid-area: icon;
  width: 70px;
}
.profile-icon::before {
  content: "";
  position: relative;
  display: block;
  padding-bottom: 100%;
  overflow: hidden;
  border-radius: 100%;
}
.profile-details {
  grid-area: details;
}
.user-details-grid {
  display: grid;
  width: 100%;
  height: 100%;
  grid-template: 1fr auto auto 1fr/ 1fr;
}
.profile-buttons {
  grid-area: buttons;
}
.profile-signout {
  grid-area: signout;
  width: 100px;
}
</style>