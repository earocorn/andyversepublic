<script>
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>Error</title>
	<meta name="description" content="Error" />
</svelte:head>

<article class="prose">
	<h1 style="color: red;">Error: {$page.status}</h1>
	<h2>{$page.error?.message}</h2>
</article>
