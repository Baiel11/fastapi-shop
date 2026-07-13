<template>
  <div class="min-h-[80vh] flex flex-col items-center justify-center px-4 text-center">
    <p class="text-8xl font-extrabold text-black mb-2">404</p>
    <h1 class="text-2xl font-bold text-black mb-3">Page Not Found</h1>
    <p class="text-gray-500 mb-10 max-w-md text-base leading-relaxed">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <router-link
      to="/"
      class="px-8 py-3 bg-black text-white border-2 border-black font-bold rounded-xl hover:bg-white hover:text-black hover:shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] transition-all"
    >
      Back to Home
    </router-link>
  </div>
</template>
