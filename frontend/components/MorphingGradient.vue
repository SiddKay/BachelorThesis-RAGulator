<template>
  <div
    ref="gradientWrapper"
    class="morphing-gradient h-screen w-screen relative overflow-hidden top-0 left-0"
    :style="wrapperStyle"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="hidden">
      <defs>
        <filter id="point">
          <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
          <feColorMatrix
            in="blur"
            mode="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8"
            result="point"
          />
          <feBlend in="SourceGraphic" in2="point" />
        </filter>
      </defs>
    </svg>
    <div class="gradients-container w-full h-full [filter:_url(#point)_blur(40px)]">
      <div class="g1" />
      <div class="g2" />
      <div class="g3" />
      <div class="g4" />
      <div class="g5" />
      <div ref="interactiveRef" class="interactive" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useMouse } from "@vueuse/core";
import { ref, watch } from "vue";

const props = withDefaults(
  defineProps<{
    firstColor?: string;
    secondColor?: string;
    thirdColor?: string;
    fourthColor?: string;
    fifthColor?: string;
    interactiveColor?: string;
    interactive?: boolean;
    size?: string;
    mixBlendMode?: string;
  }>(),
  {
    firstColor: "27, 0, 96", // dark blue #1b0060
    secondColor: "94, 4, 23", // deep red #5e0417
    thirdColor: "0, 51, 25", // dark green #003319
    fourthColor: "92, 10, 62", // dull maroon #5c0a3e
    fifthColor: "76, 19, 129", // purple #4c1381
    interactiveColor: "15, 5, 159",
    interactive: true,
    size: "80%",
    mixBlendMode: "hard-light"
  }
);

const interactiveRef = ref<HTMLDivElement>();
const { x, y } = useMouse();
const currentPos = ref({ x: 0, y: 0 });
const gradientWrapper = ref<HTMLDivElement | null>(null);

const {
  firstColor,
  secondColor,
  thirdColor,
  fourthColor,
  fifthColor,
  interactiveColor,
  interactive,
  size,
  mixBlendMode
} = toRefs(props);

const wrapperStyle = computed(() => {
  return {
    "--color1": firstColor.value,
    "--color2": secondColor.value,
    "--color3": thirdColor.value,
    "--color4": fourthColor.value,
    "--color5": fifthColor.value,
    "--color-interactive": interactiveColor.value,
    "--circle-size": size.value,
    "--blending": mixBlendMode.value
  };
});

watch(
  () => [x.value, y.value],
  () => {
    if (!interactive.value) return;
    if (!interactiveRef.value) return;
    currentPos.value.x = currentPos.value.x + (x.value - currentPos.value.x) / 20;
    currentPos.value.y = currentPos.value.y + (y.value - currentPos.value.y) / 20;
    interactiveRef.value.style.transform = `translate(${Math.round(
      currentPos.value.x
    )}px, ${Math.round(currentPos.value.y)}px)`;
  },
  {
    deep: true
  }
);
</script>

<style scoped>
.morphing-gradient {
  --space: ;
  @supports (background: linear-gradient(in oklab, #000, #fff)) {
    --space: in oklab;
  }
  --color1: 18, 113, 255;
  --color2: 221, 74, 255;
  --color3: 100, 220, 255;
  --color4: 200, 50, 50;
  --color5: 180, 180, 50;
  --color-interactive: 140, 100, 255;
  --circle-size: 80%;
  --blending: hard-light;
}

@keyframes moveInCircle {
  0% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(180deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes moveVertical {
  0% {
    transform: translateY(-50%);
  }
  50% {
    transform: translateY(50%);
  }
  100% {
    transform: translateY(-50%);
  }
}

@keyframes moveHorizontal {
  0% {
    transform: translateX(-50%) translateY(-10%);
  }
  50% {
    transform: translateX(50%) translateY(10%);
  }
  100% {
    transform: translateX(-50%) translateY(-10%);
  }
}

.morphing-gradient {
  .g1 {
    position: absolute;
    background: radial-gradient(
        circle at center,
        rgba(var(--color1), 0.8) 0,
        rgba(var(--color1), 0) 50%
      )
      no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);

    transform-origin: center center;
    animation: moveVertical 30s ease infinite;

    opacity: 1;
  }

  .g2 {
    position: absolute;
    background: radial-gradient(
        circle at center,
        rgba(var(--color2), 0.8) 0,
        rgba(var(--color2), 0) 50%
      )
      no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);

    transform-origin: calc(50% - 400px);
    animation: moveInCircle 20s reverse infinite;

    opacity: 1;
  }

  .g3 {
    position: absolute;
    background: radial-gradient(
        circle at center,
        rgba(var(--color3), 0.8) 0,
        rgba(var(--color3), 0) 50%
      )
      no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2 + 200px);
    left: calc(50% - var(--circle-size) / 2 - 500px);

    transform-origin: calc(50% + 400px);
    animation: moveInCircle 40s linear infinite;

    opacity: 1;
  }

  .g4 {
    position: absolute;
    background: radial-gradient(
        circle at center,
        rgba(var(--color4), 0.8) 0,
        rgba(var(--color4), 0) 50%
      )
      no-repeat;
    mix-blend-mode: var(--blending);

    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);

    transform-origin: calc(50% - 200px);
    animation: moveHorizontal 40s ease infinite;

    opacity: 0.7;
  }

  .g5 {
    position: absolute;
    background: radial-gradient(
        circle at center,
        rgba(var(--color5), 0.8) 0,
        rgba(var(--color5), 0) 50%
      )
      no-repeat;
    mix-blend-mode: var(--blending);

    width: calc(var(--circle-size) * 2);
    height: calc(var(--circle-size) * 2);
    top: calc(50% - var(--circle-size));
    left: calc(50% - var(--circle-size));

    transform-origin: calc(50% - 800px) calc(50% + 200px);
    animation: moveInCircle 20s ease infinite;

    opacity: 1;
  }

  .interactive {
    position: absolute;
    background: radial-gradient(
        circle at center,
        rgba(var(--color-interactive), 0.8) 0,
        rgba(var(--color-interactive), 0) 50%
      )
      no-repeat;
    mix-blend-mode: var(--blending);

    width: 100%;
    height: 100%;
    top: -50%;
    left: -50%;

    opacity: 0.7;
  }
}
</style>
