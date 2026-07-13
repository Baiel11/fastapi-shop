<template>
  <div class="min-h-[80vh] bg-white dark:bg-zinc-950 transition-colors duration-300 flex flex-col items-center justify-center px-4 text-center">
    <p class="text-8xl font-extrabold text-black dark:text-white mb-2">404</p>
    <h1 class="text-2xl font-bold text-black dark:text-white mb-3">Page Not Found</h1>
    <p class="text-gray-500 dark:text-zinc-400 mb-10 max-w-md text-base leading-relaxed">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <router-link
      to="/"
      class="px-8 py-3 bg-black dark:bg-white text-white dark:text-black border-2 border-black dark:border-white font-bold rounded-xl hover:bg-white dark:hover:bg-zinc-900 hover:text-black dark:hover:text-white hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:hover:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] transition-all cursor-pointer"
    >
      Back to Home
    </router-link>
  </div>
</template>
