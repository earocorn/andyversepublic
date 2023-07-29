<script lang='ts'>
	import '../routes/styles/ContentWrapper.css';

	export let padding: number | null;
</script>


<article class="prose-xl flex-nowrap mx-auto p-{padding}">
	<div class="container mx-auto bg-base-200 flex flex-nowrap p-3 rounded">
		<slot />
	</div>
</article>