<script setup lang="ts">
import { ref } from "vue";
import { useSessionContext } from "@/composables/useSession";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Pencil, Check, Trash2 } from "lucide-vue-next";

import { useQuestionsStore } from "@/stores/questions.store";
import type { QuestionDetail } from "@/types/api";
import AnswerCard from "@/components/AnswerCard.vue";

const { sessionId } = useSessionContext();
const props = defineProps<{ question: QuestionDetail }>();
const isEditing = ref(false);
const editedQuestion = ref(props.question.question_text);
const questionsStore = useQuestionsStore();

const handleDelete = async () => {
  if (confirm("Are you sure you want to delete this question?")) {
    await questionsStore.deleteQuestion(sessionId.value, props.question.id);
  }
};

const handleEdit = async () => {
  if (isEditing.value) {
    // Save the edited question
    await questionsStore.updateQuestion(sessionId.value, props.question.id, {
      question_text: editedQuestion.value
    });
    isEditing.value = false;
  } else {
    // Enter edit mode
    isEditing.value = true;
  }
};
</script>

<template>
  <Card class="glassmorphism">
    <CardHeader class="p-3 pb-2">
      <!-- Question -->
      <CardTitle class="flex items-center justify-between gap-2">
        <div class="flex-grow">
          <Input
            v-if="isEditing"
            v-model="editedQuestion"
            class="max-w-full"
            :placeholder="props.question.question_text"
          />
          <span v-else class="text-md font-semibold">{{ props.question.question_text }}</span>
        </div>
        <div class="flex gap-2">
          <Button
            size="xs"
            variant="ghost"
            class="text-blue-400 hover:glassmorphism hover:border-none transition-colors"
            aria-label="Edit"
            :title="isEditing ? 'Save' : 'Edit'"
            @click="handleEdit"
          >
            <component :is="isEditing ? Check : Pencil" class="h-4 w-4"
          /></Button>
          <Button
            size="xs"
            variant="ghost"
            class="text-red-400 hover:glassmorphism hover:border-none transition-colors"
            aria-label="Delete"
            title="Delete"
            @click="handleDelete"
          >
            <Trash2 class="h-4 w-4" />
          </Button>
        </div>
      </CardTitle>

      <!-- TODO: Make this section scrollable and more accessible -->
      <!-- Expected Answer -->
      <span v-if="props.question.expected_answer" class="text-sm text-gray-300"
        >Expected answer: {{ props.question.expected_answer }}
      </span>
    </CardHeader>

    <CardContent class="p-2 pt-1">
      <!-- Answers -->
      <ScrollArea class="w-full overflow-x-auto rounded-md">
        <div class="flex w-max space-x-4 p-1 pb-2.5">
          <AnswerCard
            v-for="answer in props.question.answers"
            :key="answer.configuration_id"
            :answer="answer"
            :question-id="props.question.id"
          />
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </CardContent>
  </Card>
</template>
