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
                            <md-input type="text" v-model="subjectForm" required />
                        </md-field>
                    </form>
                    <md-list>
                        <md-list-item v-for="course in courses" :key="course.dept">
                            {{course.dept}}
                        </md-list-item>
                    </md-list>
                  </md-tab>
                  <md-tab id="tab-location" md-label="Location">
                      <form>
                        <md-field>
                            <label>Location...</label>
                            <md-input type="text" v-model="locationForm" required />
                        </md-field>
                    </form>
                      <md-list>
                        <md-list-item v-for="course in courses" :key="course.dept">
                            {{course.dept}}
                        </md-list-item>
                    </md-list>
                  </md-tab>
                  <md-tab id="tab-time" md-label="Time">
                      <form>
                        <md-field>
                            <label>Time...</label>
                            <md-input type="text" v-model="timeForm" required />
                        </md-field>
                    </form>
                      <md-list>
                        <md-list-item v-for="course in courses" :key="course.dept">
                            {{course.dept}}
                        </md-list-item>
                    </md-list>
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
export default {
  name: "Home",
  data() {
    return {
        courses: [],
        sections: [],
        subjectForm: "",
        locationForm: "",
        timeForm: ""
    };
  },
  async mounted() {
    console.log(this);
    await this.fetchCourses();
    // await this.fetchSections();
  },
  methods: {
    async fetchCourses() {
      const { data } = await this.axios.get(
        "http://localhost:5000/data/courses"
      );
      console.log(data);
      this.courses = data.courses
        .filter(course => course.course_num)
        .sort(
          (courseA, courseB) =>
            this.getCourseStr(courseA.dept, courseA.course_num) <
            this.getCourseStr(courseB.dept, courseB.course_num)
        )
        .slice(0, 100);
    },
    async fetchSections() {
      const { data } = await this.axios.get(
        "http://localhost:5000/data/sections"
      );
      this.sections = data.sections;
    }
  }
};
</script>

<style>

</style>
