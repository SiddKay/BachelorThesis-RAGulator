<script setup lang="ts">
// import { useAnswersStore } from "@/stores/answers.store";
// import { useAnnotationsModalStore } from "@/stores/toggleOpen.store";

// import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
// import { MessageSquare } from "lucide-vue-next";
import type { Answer } from "@/types/api";

// Props
const props = defineProps<{ answer: Answer; questionId: string }>();

// Accessing Pinia stores
// const answersStore = useAnswersStore();
// const annotationsModalStore = useAnnotationsModalStore();

// Computed property to check if the answer has comments
// const hasComments = computed(() => !!props.answer.comments && props.answer.comments.length > 0);

// Open annotations modal
// const openAnnotationsModal = () => {
//   answersStore.selectAnswer(props.questionId, props.answer.configuration_id);
//   annotationsModalStore.open();
// };
</script>

<template>
  <Card class="w-[250px] min-h-[100px] flex-shrink-0 glassmorphism">
    <!-- Answer card header -->
    <CardHeader class="flex flex-row items-center justify-between space-y-0 p-2">
      <CardTitle class="text-sm font-medium">
        <span class="text-gray-300">Answer </span>
        <span class="text-gray-100">{{ props.answer.configuration_id }}</span></CardTitle
      >
      <!-- <Button
        variant="link"
        class="h-7 w-7 p-0 text-gray-300 hover:text-gray-50"
        aria-label="Add/view annotations"
        @click="openAnnotationsModal"
      >
        <MessageSquare :class="['h-3.5 w-3.5', hasComments ? 'fill-current' : '']" />
      </Button> -->
    </CardHeader>

    <!-- Answer card content -->
    <CardContent class="p-2.5 overflow-y-auto overflow-ellipsis">
      <p class="text">{{ props.answer.generated_answer }}</p>
    </CardContent>
  </Card>

  <!-- Modal for annotations -->
  <!-- TODO: Figure out why opening this modal completely blackens the background unlike the AddQuestionsModal -->
  <!-- <AnnotationsModal /> -->
</template>
