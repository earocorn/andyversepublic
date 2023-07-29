<svelte:head>
	<title>Inbox</title>
	<meta name="description" content="Messages Inbox"/>
</svelte:head>

<script lang="ts">
	import { onMount } from 'svelte';
	import MessageList from '../../../components/MessageList.svelte';
		

	export let data;
	$: messages = data.messages?.filter((message) => message.type === 'contact');
	$: suggestions = data.messages?.filter((message) => message.type === 'suggestion');

	onMount(() => {

	});

</script>

<div class="container">
	<div class="container p-3">
		<div class="collapse collapse-arrow bg-base-300">
		<input type="radio" name="tables" /> 
		<div class="collapse-title text-xl font-medium">
			Messages
		</div>
		<div class="collapse-content max-w-full"> 
			{#if messages}
				<MessageList type='contact' messages={messages}/>
			{/if}
		</div>
		</div>
		<div class="divider"></div>
		<div class="collapse collapse-arrow bg-base-300">
		<input type="radio" name="tables" /> 
		<div class="collapse-title text-xl font-medium">
			Suggestions
		</div>
		<div class="collapse-content max-w-full"> 
			{#if suggestions}
				<MessageList type='suggestion' messages={suggestions}/>
			{/if}
		</div>
		</div>
		{#if data.error}
		<div class="toast toast-center toast-middle">
			<div class="alert alert-error">
				<span>{data.error}</span>
			</div>
		</div>
		{/if}
	</div>
</div>