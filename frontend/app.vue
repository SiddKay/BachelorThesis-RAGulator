<script lang="ts" setup>
import MorphingGradient from "@/components/MorphingGradient.vue";
</script>

<template>
  <div class="w-screen h-screen bg-neutral-950">
    <MorphingGradient
      :firstColor="'27, 0, 96'"
      :secondColor="'246, 97, 88'"
      :thirdColor="'100, 220, 255'"
      :fourthColor="'160, 0, 102'"
      :fifthColor="'76, 19, 129'"
      :interactiveColor="'239, 180, 230'"
    />
  </div>
</template>
