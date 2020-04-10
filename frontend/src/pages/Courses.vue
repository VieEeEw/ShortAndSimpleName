<template>
	<Layout>
		<h1>Courses at UIUC</h1>
		<ul>
			<li v-for="course in courses" v-bind:key="course.dept + course.num">
				{{ course.dept + course.num }} Sections:
				<ul>
					<li v-for="section in getSectionsFor(course.dept, course.num)" v-bind:key="section.crn">
						{{ section.crn }}
					</li>
				</ul>
			</li>
		</ul>
	</Layout>
</template>

<script>
export default {
	metaInfo: {
		title: 'Courses'
	},
	data() {
		return {
			courses: [
				{
					dept: 'CS',
					num: '411'
				}
			],
			sections: [
				{
					dept: 'CS',
					num: '411',
					crn: '6558467'
				},
				{
					dept: 'CS',
					num: '412',
					crn: '6558468'
				}
			]
		};
	},
	methods: {
		getSectionsFor(dept, num) {
			console.log(this.sections);
			return this.sections.filter(section => section.dept == dept && section.num == num);
		},
		async fetchCourses() {
			const { data } = await this.axios.get('http://localhost:5000/data/courses');
			this.courses = data;
		},
		async fetchSections() {
			const { data } = await this.axios.get('http://localhost:5000/data/sections');
			this.sections = data;
		},
		async deleteCourse(dept, num) {
			const linkedSections = this.getSectionsFor(dept, num);
			const sectionDeletePromises = linkedSections.map(async section => {
				await this.deleteSection(section.crn);
			});
			await Promise.all(sectionDeletePromises);
			await this.axios.delete(`http://localhost:5000/data/course/${dept}/${num}`);
			console.log(`Course ${dept}${num} and all associated sections were deleted`);
		},
		async deleteSection(crn) {
			await this.axios.delete(`http://localhost:5000/data/section/${crn}`);
			console.log(`Section ${crn} deleted`);
		}
	}
};
</script>
