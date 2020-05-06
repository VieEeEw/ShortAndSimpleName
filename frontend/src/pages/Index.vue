<template>
  <Layout :markers="markers" :paths="paths">
    <h1>This is the home page</h1>
    <p>
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Pariatur excepturi labore tempore expedita, et iste
      tenetur suscipit explicabo! Dolores, aperiam non officia eos quod asperiores
    </p>
    <md-button v-on:click="plotIntersection">Plot Intersection</md-button>
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
      paths: []
    };
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
            bl1: [38331, 58598],
            bl2: [65299, 34572]
          },
          { withCredentials: true }
        );
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
</style>
