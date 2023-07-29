<script lang='ts'>
	import { onMount } from "svelte";
	import '../styles/Profile.css';
	import { currentUser } from "../../server/stores";
	import type AndyVerseUser from "../../server/models/AndyVerseUser";
	
	let dashUser: AndyVerseUser|null = null;

	onMount(() => {
		currentUser.subscribe((val) => {
			dashUser = val;
		});
	})

</script>

<svelte:head>
	<title>My Profile</title>
	<meta name="description" content="My Profile" />
</svelte:head>

<h3>Welcome to your dashboard{dashUser ? (', ' + dashUser.username) + '!' : '!'}</h3>