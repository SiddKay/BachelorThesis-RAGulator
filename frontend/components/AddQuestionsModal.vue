<script setup lang="ts">
/**----------------------------- Imports ----------------------------------- */
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useQuestionsStore } from "@/stores/questionsStore";
import { useQuestionsModalStore } from "@/stores/toggleOpenStore";

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
// import { Checkbox } from "@/components/ui/checkbox";
import { X, Plus } from "lucide-vue-next";

/**----------------------------- refs ----------------------------------- */

const newQuestions = ref([{ text: "", important: false }]);

/**----------------------------- Methods ----------------------------------- */

// Accessing Pinia stores
const questionsModalStore = useQuestionsModalStore();
const { isOpen: isModalOpen } = storeToRefs(questionsModalStore);

const questionsStore = useQuestionsStore();
const { isProcessing } = storeToRefs(questionsStore);

// Methods for managing questions
const addNewQuestion = () => {
  newQuestions.value.push({ text: "", important: false });
};

const removeNewQuestion = (index: number) => {
  newQuestions.value.splice(index, 1);
};

const saveNewQuestions = () => {
  const validNewQuestions = newQuestions.value.filter((q) => q.text.trim() !== "");
  questionsStore.addQuestions(validNewQuestions);
  questionsModalStore.close();
  newQuestions.value = [{ text: "", important: false }];
};

// Handle file upload
const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    questionsStore.handleFileUpload(file);
  }
};
</script>

<template>
  <Dialog :open="isModalOpen" @update:open="questionsModalStore.close">
    <DialogContent class="glassmorphism-modal sm:max-w-[425px]">
      <!-- Modal Header -->
      <DialogHeader>
        <DialogTitle>Add Questions</DialogTitle>
        <DialogDescription class="text-gray-300">
          Add new questions manually or upload a CSV file.
        </DialogDescription>
      </DialogHeader>

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
        <TabsContent value="manual">
          <div class="space-y-4">
            <div
              v-for="(question, index) in newQuestions"
              :key="index"
              class="flex items-center space-x-2"
            >
              <Input
                v-model="question.text"
                placeholder="Enter question"
                class="flex-grow placeholder:text-gray-400"
              />
              <!-- <Checkbox :id="`important-${index}`" v-model="question.important" />
              <label :for="`important-${index}`">Important</label> -->
              <Button
                variant="link"
                size="icon"
                class="text-gray-300 hover:text-gray-50"
                @click="removeNewQuestion(index)"
              >
                <X class="h-4 w-4 p-0 m-0" />
              </Button>
            </div>
            <Button
              size="xs"
              variant="ghost"
              class="text-sm [text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none"
              @click="addNewQuestion"
            >
              <Plus class="mr-2 h-4 w-4" />Add Question</Button
            >
          </div>
        </TabsContent>

        <!-- Upload questions from a CSV file -->
        <TabsContent value="upload">
          <div class="space-y-4">
            <Input type="file" accept=".csv" @change="handleFileUpload" />
            <p class="ml-0.5 text-sm text-gray-300">Upload a CSV file containing questions.</p>
          </div>
        </TabsContent>
      </Tabs>

      <!-- Modal footer -->
      <DialogFooter>
        <Button
          variant="ghost"
          class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none"
          @click="questionsModalStore.close"
          >Cancel</Button
        >
        <Button
          variant="secondary"
          class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_0%)] border-none"
          :disabled="isProcessing"
          @click="saveNewQuestions"
          >Save</Button
        >
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
