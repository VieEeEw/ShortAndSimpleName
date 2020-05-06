<template>
  <Layout :markers="markers" :paths="paths">
    <h1>High-Five Calculator</h1>
    <p>Provide a schedule of CRNs for you and a friend, if your schedules are compatible, this tool will show you where you can high-five on your way to class!</p>
    <br />
    <form @submit="plotIntersection">
      <div class="schedule-grid">
        <div>
          <h3>You</h3>
          <md-field :key="index" v-for="(crn, index) in bl1">
            <label>Your CRN {{index}}</label>
            <md-input type="number" v-model="bl1[index]" />
          </md-field>
        </div>
        <div>
          <h3>Friend</h3>
          <md-field :key="index" v-for="(crn, index) in bl2">
            <label>Friend CRN {{index}}</label>
            <md-input type="number" v-model="bl2[index]" />
          </md-field>
        </div>
      </div>
      <md-button
        class="md-primary md-raised"
        style="width:100%; position:relative; left:-10px;"
        type="submit"
      >Calculate High-Five</md-button>
    </form>
    <div class="response-text">{{this.error}}</div>
  </Layout>
</template>

<script>
function toMarker(data) {
  return {
    position: {
      lat: data.lat,
      lng: data.long || data.lng
    }
  };
}

export default {
  metaInfo: {
    title: "Home"
  },
  data: function() {
    return {
      markers: [],
      paths: [],
      bl1: [null, null],
      bl2: [null, null],
      error: ""
    };
  },
  mounted() {
    // Update form field length to always provide avaiable CRN inputs
    setInterval(() => {
      this.bl1 = this.bl1.filter(elt => !!elt);
      this.bl2 = this.bl2.filter(elt => !!elt);
      this.bl1.push(null);
      this.bl2.push(null);
    }, 100);
  },
  methods: {
    async plotIntersection(e) {
      e.preventDefault();
      console.log(this);
      this.markers = [];
      this.paths = [];
      try {
        const {
          data: { intersections }
        } = await this.axios.post(
          "http://app.dev.localhost:5000/data/intersection",
          {
            bl1: this.bl1.filter(crn => crn !== null),
            bl2: this.bl2.filter(crn => crn !== null)
            // bl1: [38331, 58598],
            // bl2: [65299, 34572]
          },
          { withCredentials: true }
        );

        if (intersections.length == 0) {
          this.error = "No intersection";
          return;
        }

        try {
          intersections.forEach(intersection => {
            const intersectionMarker = toMarker(intersection.intersection);
            const studPaths = [
              intersection.student1,
              intersection.student2
            ].map(stud =>
              stud.steps.map(step => [
                { lat: step.from.lat, lng: step.from.long },
                { lat: step.to.lat, lng: step.to.long }
              ])
            );

            const student1Start = toMarker(studPaths[0].flat().slice(0)[0]);
            const student1End = toMarker(studPaths[0].flat().slice(-1)[0]);

            const student2Start = toMarker(studPaths[1].flat().slice(0)[0]);
            const student2End = toMarker(studPaths[1].flat().slice(-1)[0]);

            this.paths.push(...studPaths[0], ...studPaths[1]);
            this.markers.push(
              intersectionMarker,
              student1Start,
              student1End,
              student2Start,
              student2End
            );
          });
        } catch (err) {
          console.error(err);
        }
      } catch (err) {
        alert(err.response.data.error);
      }
    }
  }
};
</script>

<style>
.home-links a {
  margin-right: 1rem;
}
.response-text {
  width: 100%;
  text-align: center;
  margin-top: 25px;
  color: red;
}
.schedule-grid {
  display: grid;
  position: relative;
  grid-template-columns: 1fr 1fr;
  grid-column-gap: 15px;
}
</style>
