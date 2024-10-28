<script setup lang="ts">
import type { IQuestion } from "@/interfaces/EvaluationSession.interface";
import AnswerCard from "./AnswerCard.vue";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Star } from "lucide-vue-next";

const props = defineProps<{ question: IQuestion }>();
</script>

<template>
  <Card class="glassmorphism">
    <CardHeader class="p-3 pb-2">
      <!-- Question -->
      <CardTitle class="flex items-center justify-between">
        <span class="text-md font-semibold">{{ props.question.text }}</span>
        <Star v-if="props.question.important" class="h-5 w-5 text-yellow-400" />
      </CardTitle>

      <!-- TODO: Make this section scrollable and more accessible -->
      <!-- Expected Answer -->
      <span v-if="props.question.expectedAnswer" class="text-sm text-gray-300"
        >Expected answer: {{ props.question.expectedAnswer }}
      </span>
    </CardHeader>

    <CardContent class="p-2 pt-1">
      <!-- Answers -->
      <ScrollArea class="w-full overflow-x-auto rounded-md">
        <div class="flex w-max space-x-4 p-1 pb-2.5">
          <AnswerCard
            v-for="answer in props.question.answers"
            :key="answer.configVersion"
            :answer="answer"
            :question-id="props.question.id"
          />
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </CardContent>
  </Card>
</template>
