<svelte:head>
	<title>Contact</title>
	<meta name="description" content="Contact Form" />
</svelte:head>

<script lang="ts">
	import { onMount } from "svelte";

	//change to use sveltekit form actions
	import ContentWrapper from "../../components/ContentWrapper.svelte";
	import { emailRegex } from "../../server/config/help";
	import { postContactMessage } from "../../server/services/MessageHandler";

	let errorMsg: [string, string, boolean] = ['', '', false];
	let formData: [string, string, string] = ['', '', ''];

	onMount(() => {
		resetErrorMsg();
		resetFormData();
	});

	async function handleSubmit() {
		if(formData[2].length < 1 || formData[1].length < 1 || formData[0].length < 1) {
			errorMsg = ['warning', 'Please fill in all fields.', false];
			return;
		}
		if(!emailRegex.test(formData[1])) {
			errorMsg = ['warning', 'Please enter a valid email.', false];
			return;
		}
		try {
			const response = await postContactMessage(formData[2], formData[1], formData[0]);
			if(response === 'success') {
				console.info('successfully posted message')
				errorMsg = [response, 'Message has been sent!', true];
				resetFormData();
				await new Promise((resolve) => setTimeout(resolve, 5000));
				resetErrorMsg();
			} else {
				errorMsg = ['error', response, true]
				await new Promise((resolve) => setTimeout(resolve, 3000));
				resetErrorMsg();
			}
		} catch (error) {
			console.error(error);
			errorMsg = ['error', 'Unknown error', false]
		}
	}

	function resetErrorMsg() {
		errorMsg = ['', '', false];
	}

	function resetFormData() {
		formData = ['', '', ''];
	}

</script>

<ContentWrapper padding={0}>
	<div class="container">
		<div class="text-center">
			<h1>Contact</h1>
		</div>
		<div class="container text-center lg:w-1/2 m-auto">
			<div class="form-control">
				<label for="name" class="label">
				  <span class="label-text">Name*</span>
				</label>
				<input on:input={resetErrorMsg} bind:value={formData[0]} required type="text" id="name" placeholder="name" class="input input-bordered" />
			  </div>
			  <div class="form-control">
				<label class="label" for="email">
				  <span class="label-text">Email*</span>
				</label>
				<input on:input={resetErrorMsg} bind:value={formData[1]} required type="email" id="email" placeholder="email" class="input input-bordered"/>
			  </div>
			  <div class="form-control">
                <label class="label" for="message">
					<span class="label-text">Message*</span>
				  </label>
                <textarea on:input={resetErrorMsg} bind:value={formData[2]} required id="message" rows="7" class="textarea textarea-bordered" placeholder="type your message here"></textarea>
            </div>
			{#if errorMsg[0].length > 0}
				<div class="alert alert-{errorMsg[0]}">{errorMsg[1]}</div>
			{/if}
			  <div class="form-control mt-6">
				<button class="btn btn-primary" disabled={errorMsg[2]} on:click={() => handleSubmit()}>Submit</button>
			  </div>
		</div>
	</div>
</ContentWrapper>