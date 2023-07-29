<svelte:head>
	<title>Login</title>
	<meta name="description" content="Login Page" />
</svelte:head>

<script lang="ts">
	import { browser } from "$app/environment";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import ContentWrapper from "../../components/ContentWrapper.svelte";
	import { handleSignIn } from "../../server/authentication/authenticator";
	import { auth } from "../../server/config/firebase";
	import { onAuthStateChanged } from "firebase/auth";

	let errorMsg = ['', ''];
	let emailValue = '';
	let passwordValue = '';

	onMount(() => {
		errorMsg = ['', ''];
		emailValue = '';
		passwordValue = '';
		
		onAuthStateChanged(auth, (user) => {
			if(user) {
				if(browser) {
					goto('/home');
				}
			}
		})
	})

	async function handleSubmit() {
		const response = await handleSignIn(auth, emailValue, passwordValue);
		if(response !== 'success') {
			errorMsg = ['error', response];
			return;
		}
		errorMsg = ['success', 'Success! Logging in...'];
		emailValue = '';
		passwordValue = '';
		if(browser) {
			goto('/home');
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
	<div class="container flex-col">
	<div class="container text-center">
		<h1 class="">Sign in to AndyVerse</h1>
	</div>
	<div class="card flex-shrink-0 w-full mx-auto max-w-sm shadow-2xl bg-base-100">
		<div class="card-body">
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
				<div class="form-control">
					<!-- svelte-ignore a11y-label-has-associated-control -->
					<label class="label">
						<span class="label-text">Password</span>
					</label>
					<input
						type="password"
						placeholder="password"
						class="input input-bordered"
						bind:value={passwordValue}
						on:keydown={submitWithKey}
					/>
					<!-- svelte-ignore a11y-label-has-associated-control -->
					<label class="label">
						<a href="/resetpassword" class="label-text-alt link">Forgot password?</a>
					</label>
				</div>
				{#if errorMsg[1].length > 0}
					<div class="alert alert-{errorMsg[0]}">{errorMsg[1]}</div>
				{/if}
				<div class="form-control mt-6">
					<button class="btn btn-primary" on:click={handleSubmit}>Sign in</button>
				</div>
			</form>
		</div>
	</div>
</div>
</ContentWrapper>