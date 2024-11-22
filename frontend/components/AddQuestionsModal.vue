<script setup lang="ts">
/**----------------------------- Imports ----------------------------------- */
import { ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { useQuestionsStore } from "@/stores/questions.store";
import { useQuestionsModalStore } from "@/stores/toggleOpen.store";
import type { QuestionCreate } from "@/types/api";
import type { UUID } from "crypto";

// Importing UI components
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Trash2, Plus } from "lucide-vue-next";

/**----------------------------- Setup ----------------------------------- */

const questionsModalStore = useQuestionsModalStore();
const { isOpen: isModalOpen } = storeToRefs(questionsModalStore);

const questionsStore = useQuestionsStore();
const { isLoading } = storeToRefs(questionsStore);

// TODO: Get sessionId from Nuxt page context
const sessionId = ref<UUID>("dd276a29-4cbb-4526-b922-f126827657fb" as UUID);

const newQuestions = ref<QuestionCreate[]>([
  {
    question_text: "",
    expected_answer: ""
  }
]);
const uploadError = ref<string | null>(null);

/**----------------------------- Methods ----------------------------------- */
const addNewQuestion = () => {
  newQuestions.value.push({
    question_text: "",
    expected_answer: ""
  });
};

const removeNewQuestion = (index: number) => {
  if (newQuestions.value.length > 1) {
    newQuestions.value.splice(index, 1);
  }
};

const saveNewQuestions = async () => {
  const validNewQuestions = newQuestions.value.filter((q) => q.question_text.trim() !== "");

  if (validNewQuestions.length === 0) {
    uploadError.value = "Please enter at least one question.";
    return;
  }

  try {
    await questionsStore.createQuestionsBulk(sessionId.value, validNewQuestions);
    resetModal();
  } catch (error) {
    uploadError.value = "Failed to save questions. With error: " + error;
  }
};

const resetModal = () => {
  questionsModalStore.close();
  newQuestions.value = [{ question_text: "", expected_answer: "" }];
  uploadError.value = null;
};

// Handle file upload
// const handleFileUpload = async (event: Event) => {
//   const file = (event.target as HTMLInputElement).files?.[0];
//   if (!file) return;

//   try {
//     uploadError.value = null;
//     if (file) {
//       await questionsStore.handleFileUpload(file);
//     }
//     resetModal();
//   } catch (error) {
//     uploadError.value = "Failed to upload file: " + error;
//   } finally {
//     (event.target as HTMLInputElement).value = "";
//   }
// };

// Reset questions if modal is closed without saving
watch(isModalOpen, (isOpen) => {
  if (!isOpen) resetModal();
});
</script>

<template>
  <Dialog :open="isModalOpen" @update:open="questionsModalStore.close">
    <DialogContent class="glassmorphism-modal sm:max-w-[60vw] max-h-[80vh] flex flex-col">
      <!-- Modal Header -->
      <DialogHeader>
        <DialogTitle>Add Questions</DialogTitle>
        <DialogDescription class="text-gray-300">
          Add new questions manually or upload a CSV file.
        </DialogDescription>
      </DialogHeader>

      <!-- Error display -->
      <div v-if="uploadError" class="text-red-400 text-sm mb-2">
        {{ uploadError }}
      </div>

      <!-- Different upload modes -->
      <Tabs default-value="manual" class="w-full">
        <TabsList class="grid w-full grid-cols-2 glassmorphism border-none">
          <TabsTrigger
            value="manual"
            class="text-white [text-shadow:_0_1px_2px_rgb(0_0_0_/_60%)] data-[state=active]:[text-shadow:_0_1px_1px_rgb(0_0_0_/_0%)]"
            >Manual</TabsTrigger
          >
          <TabsTrigger
            value="upload"
            class="text-white [text-shadow:_0_1px_2px_rgb(0_0_0_/_60%)] data-[state=active]:[text-shadow:_0_1px_1px_rgb(0_0_0_/_0%)]"
            >Upload CSV</TabsTrigger
          >
        </TabsList>

        <!-- Manual question entry -->
        <TabsContent value="manual" class="max-h-[30vh] overflow-hidden">
          <div class="space-y-4 py-2 max-h-[28vh] overflow-y-auto">
            <!-- Individual Question-Answer Input -->
            <div
              v-for="(question, index) in newQuestions"
              :key="index"
              class="flex flex-1 px-1 items-center space-x-2"
            >
              <Input
                v-model="question.question_text"
                placeholder="Enter question"
                class="flex-grow placeholder:text-gray-400"
                :disabled="isLoading"
              />
              <Input
                v-model="question.expected_answer"
                placeholder="Enter expected answer"
                class="flex-grow placeholder:text-gray-400"
              />
              <Button
                variant="link"
                size="icon"
                class="text-gray-300 hover:text-red-400"
                :disabled="isLoading || newQuestions.length === 1"
                @click="removeNewQuestion(index)"
              >
                <Trash2 class="h-4 w-4 p-0 m-0" />
              </Button>
            </div>
          </div>
        </TabsContent>

        <!-- Upload questions from a CSV file -->
        <TabsContent value="upload">
          <div class="space-y-4">
            <p class="ml-0.5 text-sm text-gray-300">File upload functionality coming soon.</p>
            <!-- TODO: Add: file upload logic and Figure out how to change the default black color of Input button -->
            <!-- <Input type="file" accept=".csv" :disabled="isProcessing" @change="handleFileUpload" />
            <p class="ml-0.5 text-sm text-gray-300">Upload a CSV file containing questions.</p> -->
          </div>
        </TabsContent>
      </Tabs>

      <!-- Modal footer -->
      <DialogFooter>
        <div class="flex justify-between w-full">
          <Button
            variant="ghost"
            class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none select-none touch-none"
            :disabled="isLoading"
            @click="addNewQuestion"
          >
            <Plus class="mr-2 h-4 w-4" />Add Question
          </Button>
          <div class="flex space-x-2">
            <Button
              variant="ghost"
              class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none select-none touch-none"
              :disabled="isLoading"
              @click="questionsModalStore.close"
            >
              Cancel
            </Button>
            <Button
              variant="secondary"
              class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_0%)] border-none select-none touch-none"
              :disabled="isLoading"
              @click="saveNewQuestions"
            >
              Save
            </Button>
          </div>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
