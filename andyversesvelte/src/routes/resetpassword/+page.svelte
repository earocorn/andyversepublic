<svelte:head>
	<title>Forgot Password</title>
	<meta name="description" content="Reset Password" />
</svelte:head>

<script lang="ts">
	import { onMount } from "svelte";
	import ContentWrapper from "../../components/ContentWrapper.svelte";
	import { auth } from "../../server/config/firebase";
	import { sendPasswordResetEmail } from "firebase/auth";
	import { goto } from "$app/navigation";
	import { browser } from "$app/environment";

	let emailValue = '';
	//type (error, success) and message
	let errorMsg = ['', ''];

	onMount(() => {
		emailValue = '';
		errorMsg = ['', ''];
	});

	async function handleSubmit() {
		try{
			sendPasswordResetEmail(auth, emailValue)
			.then(() => {
				errorMsg = ['success', 'Successfully sent password reset email! Redirecting...'];
				if(browser) {
					setTimeout(() => (goto('/home')), 3500)
				}
			})
			.catch((error) => {
				errorMsg = ['error', 'Invalid email, please try again!'];
			});
		}
		catch(error) {
			errorMsg = ['error', 'There was an error submitting your request.']
		}
	}

	function submitWithKey(event: KeyboardEvent) {
		if(event.key === 'Enter') {
			handleSubmit();
		} else {
			errorMsg = ['', ''];
		}
	}
</script>

<ContentWrapper padding={3}>
	<div class="container">
	<div class="container text-center">
		<h1 class="">Password Reset</h1>
	</div>
	<div class="card flex-shrink-0 w-full mx-auto max-w-sm shadow-2xl bg-base-100">
		<div class="card-body">
			<div class="card-title">Please enter your email</div>
			<form class="form" on:submit|preventDefault={handleSubmit}>
				<div class="form-control">
					<!-- svelte-ignore a11y-label-has-associated-control -->
					<label class="label">
						<span class="label-text">Email</span>
					</label>
					<input 
					type="email" 
					placeholder="email" 
					class="input input-bordered"
					bind:value={emailValue} 
					on:keydown={submitWithKey}
					/>
				</div>
				
				{#if errorMsg[0].length > 0}
					<div class="alert alert-{errorMsg[0]}">{errorMsg[1]}</div>
				{/if}
				<div class="form-control mt-6">
					<button class="btn btn-primary" on:click={handleSubmit}>Submit</button>
				</div>
			</form>
			<a href="https://firebase.google.com/support/privacy" target="_blank" class="link link-info text-center text-sm">Firebase Data Protection</a>
		</div>
	</div>
</div>
</ContentWrapper>