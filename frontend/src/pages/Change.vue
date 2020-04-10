<template>
	<Layout>
		<h1>Change Password</h1>
		<p>
			<form @submit="changeUser">
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
					<label for="password">Enter your new password: </label>
					<input 
						type="password" 
						name="password" 
						@change="updateForm"
						required 
					>
				</div>
    
				<div>
					<input type="submit" value="Change">
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
		title: 'Change'
	},
	data() {
		return {
			net_id: '',
			password: '',
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
            async changeUser(e) {
				e.preventDefault();
				// Get form data from the component object
				let {net_id, password} = this;
				try {
					// Try to POST the new user 🤞
					const body = { net_id, password }
					const { data } = await this.axios.post('http://localhost:5000/auth/update-pswd', body);
					this.response = data;
					// Nasty UX (just using for development right now)
					alert("Successfully changed password!")
					window.location.href = '/';
				} catch (err) {
					// Oops, something went wrong. Tell the user 😫
					this.response = err.response.data.error;
				}
			}
        }
};
</script>