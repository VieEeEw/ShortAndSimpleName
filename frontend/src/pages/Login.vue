<template>
	<Layout>
		<h1>Login</h1>
		<p>
			<form action="http://localhost:5000/auth/login" method="get">
				<div>
					<label for="net_id">Enter your NetID: </label>
					<input type="text" name="net_id" id="net_id" required>
				</div>
				<div>
					<label for="password">Enter your password: </label>
					<input type="password" name="password" id="password" required>
				</div>
				<div>
					<input type="submit" value="Login">
				</div>
			</form>
		</p>
	</Layout>
</template>

<script>
export default {
	metaInfo: {
		title: 'Login'
	}
};
</script>
