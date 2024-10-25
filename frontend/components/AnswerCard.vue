<script setup lang="ts">
import { useQuestionsStore } from "@/stores/questionsStore";
import { useAnnotationsModalStore } from "@/stores/toggleOpenStore";

import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { MessageSquare } from "lucide-vue-next";
import type { IAnswer } from "@/interfaces/EvaluationSession.interface";

// Props
const props = defineProps<{ answer: IAnswer; questionId: number }>();

// Accessing Pinia stores
const questionsStore = useQuestionsStore();
const annotationsModalStore = useAnnotationsModalStore();

// Methods

// Open annotations modal
const openAnnotationsModal = () => {
  questionsStore.selectAnswer(props.questionId, props.answer.configVersion);
  annotationsModalStore.open();
};
</script>

<template>
  <Card class="w-[250px] min-h-[100px] flex-shrink-0 glassmorphism">
    <!-- Answer card header -->
    <CardHeader class="flex flex-row items-center justify-between space-y-0 p-2">
      <CardTitle class="text-sm font-medium">
        <span class="text-gray-300">Answer </span>
        <span class="text-gray-100">{{ props.answer.configVersion }}</span></CardTitle
      >
      <Button
        variant="link"
        class="h-7 w-7 p-0 text-gray-300 hover:text-gray-50"
        @click="openAnnotationsModal"
      >
        <MessageSquare class="h-3.5 w-3.5" />
      </Button>
    </CardHeader>

    <!-- Answer card content -->
    <CardContent class="p-2.5 overflow-y-auto overflow-ellipsis">
      <p class="text">{{ props.answer.text }}</p>
    </CardContent>
  </Card>

  <!-- Modal for annotations -->
  <!-- TODO: Figure out why opeing this modal completely blackens the background unlike the AddQuestionsModal -->
  <AnnotationsModal />
</template>
