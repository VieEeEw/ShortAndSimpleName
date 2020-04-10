<template>
	<Layout>
		<h1>Register</h1>
		<p>
			<form @submit="registerUser">
				<div>
					<label for="net_id">Enter your NetID: </label>
					<input 
						type="text" 
						name="net_id" id="net_id" 
						@change="updateForm"
						required
					>
				</div>
				<div>
					<input type="submit" value="Delete">
				</div>
			</form>
			<pre>
				{{response}}
			</pre>
		</p>
	</Layout>
</template>

<script>
export default {
	metaInfo: {
		title: 'Delete'
	},
	data() {
		return {
			net_id: '',
			response: ''
		};
	},
	methods: {
			updateForm(e) {
				e.preventDefault();
				// Store form state in the component's data
				const fieldName = e.target.name;
				const currentValue = e.target.value;
				this[fieldName] = currentValue;
			},
            async registerUser(e) {
				e.preventDefault();
				// Get form data from the component object
				let {net_id} = this;
				try {
					// Try to POST the new user 🤞
					const body = { net_id }
					const { data } = await this.axios.post('http://localhost:5000/auth/delete', body);
					this.response = data;
					// Nasty UX (just using for development right now)
					alert("Your account has been deleteed!")
					window.location.href = '/';
				} catch (err) {
					// Oops, something went wrong. Tell the user 😫
					this.response = err.response.data.error;
				}
			}
        }
};
</script>