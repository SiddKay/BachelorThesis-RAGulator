<script setup lang="ts">
/**----------------------------- Imports ----------------------------------- */
import { ref, watch } from "vue";
import { storeToRefs } from "pinia";
import type { QuestionCreate } from "@/types/api";
import { useQuestionsStore } from "@/stores/questions.store";
import { useQuestionsModalStore } from "@/stores/toggleOpen.store";
import { useSessionContext } from "@/composables/useSession";

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
import { Trash2, Plus } from "lucide-vue-next";

/**----------------------------- Setup ----------------------------------- */

const { sessionId } = useSessionContext();

const questionsModalStore = useQuestionsModalStore();
const { isOpen: isModalOpen } = storeToRefs(questionsModalStore);

const questionsStore = useQuestionsStore();
const { isLoading } = storeToRefs(questionsStore);

const newQuestions = ref<QuestionCreate[]>([
  {
    question_text: "",
    expected_answer: ""
  }
]);
const uploadError = ref<string | null>(null);

const activeTab = ref("manual");
const fileInput = ref<HTMLInputElement | null>(null);

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
const handleFileUpload = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) return;

  try {
    uploadError.value = null;
    const parsedQuestions = await questionsStore.handleFileUpload(file);
    newQuestions.value = parsedQuestions;
    activeTab.value = "manual";
  } catch (error) {
    uploadError.value = error as string;
  } finally {
    if (fileInput.value) fileInput.value.value = "";
  }
};

// Reset questions if modal is closed without saving
watch(isModalOpen, (isOpen) => {
  if (!isOpen) resetModal();
});
</script>

<template>
  <Dialog :open="isModalOpen" @update:open="questionsModalStore.close">
    <DialogContent class="glassmorphism-modal sm:max-w-[50vw] max-h-[80vh] flex flex-col">
      <!-- Modal Header -->
      <DialogHeader>
        <DialogTitle>Add Questions Manually</DialogTitle>
        <DialogDescription class="text-gray-300">
          Add new questions manually or upload a CSV file with "Question" and "Expected Answer"
          columns.
        </DialogDescription>
      </DialogHeader>

      <!-- Error display -->
      <div v-if="uploadError" class="text-red-400 text-sm mb-2">
        {{ uploadError }}
      </div>

      <!-- Questions list -->
      <div class="max-h-[30vh] overflow-hidden">
        <div class="space-y-4 py-2 max-h-[28vh] overflow-y-auto">
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
      </div>

      <!-- Modal footer -->
      <DialogFooter>
        <div class="flex justify-between w-full">
          <div class="flex items-center space-x-2">
            <Button
              variant="ghost"
              class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none select-none touch-none"
              :disabled="isLoading"
              @click="addNewQuestion"
            >
              <Plus class="mr-2 h-4 w-4" />Add Question
            </Button>
            <span class="mx-2 text-gray-400">or</span>
            <input
              ref="fileInput"
              type="file"
              accept=".csv"
              class="hidden"
              @change="handleFileUpload"
            >
            <Button
              variant="ghost"
              class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none select-none touch-none"
              :disabled="isLoading"
              @click="fileInput?.click()"
            >
              Import CSV
            </Button>
          </div>
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
