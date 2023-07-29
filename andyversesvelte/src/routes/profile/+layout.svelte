<script lang='ts'>
	import { afterUpdate, onMount } from "svelte";


	import ContentWrapper from "../../components/ContentWrapper.svelte";
	import { currentUser } from "../../server/stores";
	import type AndyVerseUser from "../../server/models/AndyVerseUser";
	import { dashboardRoutes } from "../../server/config/routes";
	import { handleSignOut } from "../../server/authentication/authenticator";
	
    let active = 'profile';
	let dashUser: AndyVerseUser|null = null;
    let activeTitle = 'Dashboard';
	let toggle: boolean = false;

	onMount(() => {

		currentUser.subscribe((val) => {
			dashUser = val;
		});
	});

    afterUpdate(() => {
        const pathFormatted = location.pathname.split('/')[2] || 'profile'
        active = pathFormatted;
        const activeDashboardRoute = dashboardRoutes.find((route) => {
            return route[0] === active;
        });
        activeTitle = activeDashboardRoute ? activeDashboardRoute[1] : 'Dashboard';
    });
    
</script>

<main>
<ContentWrapper padding={2}>
	<div class="container mx-auto">
		<div class="drawer lg:drawer-open bg-base-300">
		<input id="dashboard-drawer" type="checkbox" bind:checked={toggle} class="drawer-toggle"/>
		<div class="drawer-content w-full bg-base-200">
			<label for="dashboard-drawer" class="btn btn-ghost link w-full drawer-button" data-tip="Click me to get started!" style="font-size: x-large;">
                {activeTitle}
                <svg
                width="12px"
                height="12px"
                class="h-4 w-4 fill-current sm:inline-block lg:hidden"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 2048 2048"
                ><path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z" /></svg
            ></label>
            <div class="divider"/>
			<slot/>
		</div> 
		<div class="drawer-side flex-row">
			<label for="dashboard-drawer" class="drawer-overlay"></label>
			<ul class="menu profilemenu my-auto h-full justify-center text-base-content">
				<!-- Sidebar content here -->
                {#each dashboardRoutes as dashRoute}
                     <li><a on:click={() => toggle = false} href="/profile/{dashRoute[0]}" class="{active === dashRoute[0] ? 'active' : ''}">{dashRoute[1]}</a></li>
                {/each}
				<!-- svelte-ignore a11y-invalid-attribute -->
				<li><a on:click={() => {
				}} class="bg-primary" on:click={handleSignOut} href="#">Sign Out</a></li>
			</ul>
		
		</div>
		</div>
	</div>
	
</ContentWrapper>
</main>
