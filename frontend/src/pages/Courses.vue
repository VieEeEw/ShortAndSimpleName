<template>
  <Layout>
    <h1>Add/Modify Course</h1>
    <form @submit="modifyCourse">
      <div>
        <label for="dept">Course Department</label>
        <input type="text" name="dept" @change="updateModifyForm" required />
      </div>
      <div>
        <label for="course_num_old">Course Number</label>
        <input type="text" name="course_num_old" @change="updateModifyForm" required />
      </div>
      <div>
        <label for="course_num">New Course Number (if modifying)</label>
        <input type="text" name="course_num_new" @change="updateModifyForm" />
      </div>
      <div>
        <input type="submit" value="Update" />
      </div>
    </form>
    <h1>List of Courses at UIUC</h1>
    <ul>
      <li v-for="course in courses" v-bind:key="course.dept + course.course_num">
        {{ getCourseStr(course.dept, course.course_num) }}
        <a
          href="#"
          :data-dept="course.dept"
          :data-course_num="course.course_num"
          v-on:click="deleteHander"
        >X</a>
        <!-- Sections:
        <ul>
          <li
            v-for="section in getSectionsFor(course.dept, course.course_num)"
            v-bind:key="section.crn"
          >{{ section.crn }}</li>
        </ul>-->
      </li>
    </ul>
  </Layout>
</template>

<script>
export default {
  metaInfo: {
    title: "Courses"
  },
  data() {
    return {
      courses: [],
      sections: [],
      modifyForm: {
        dept: "",
        course_num_old: "",
        course_num_new: ""
      }
    };
  },
  async mounted() {
    console.log(this);
    await this.fetchCourses();
    // await this.fetchSections();
  },
  methods: {
    async modifyCourse(e) {
      e.preventDefault();
      const { dept, course_num_old, course_num_new } = this.modifyForm;
      const body = { course_num: course_num_new || course_num_old };
      const requestFn = course_num_new ? this.axios.patch : this.axios.put;
      const { data } = await requestFn(
        `http://localhost:5000/data/course/${dept}/${course_num_old}`,
        body
      );
      await this.fetchCourses();
    },
    updateModifyForm(e) {
      e.preventDefault();
      const fieldName = e.target.name;
      const currentVal = e.target.value;
      this.modifyForm[fieldName] = currentVal;
    },
    async deleteHander(e) {
      const { dept, course_num } = e.target.dataset;
      await this.deleteCourse(dept, course_num);
      await this.fetchCourses();
    },
    getSectionsFor(dept, course_num) {
      return this.sections.filter(
        section => section.dept == dept && section.course_num == course_num
      );
    },
    getCourseStr(dept, course_num) {
      return `${dept}${course_num}`;
    },
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
    },
    async deleteCourse(dept, course_num) {
      const linkedSections = this.getSectionsFor(dept, course_num);
      const sectionDeletePromises = linkedSections.map(async section => {
        await this.deleteSection(section.crn);
      });
      await Promise.all(sectionDeletePromises);
      await this.axios.delete(
        `http://localhost:5000/data/course/${dept}/${course_num}`
      );
      console.log(
        `Course ${dept}${course_num} and all associated sections were deleted`
      );
    },
    async deleteSection(crn) {
      //   await this.axios.delete(`http://localhost:5000/data/section/${crn}`);
      //   console.log(`Section ${crn} deleted`);
    }
  }
};
</script>
