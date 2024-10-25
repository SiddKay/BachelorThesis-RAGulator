<script setup lang="ts">
/**----------------------------- Imports ----------------------------------- */
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useQuestionsStore } from "@/stores/questionsStore";
import { useAnnotationsModalStore } from "@/stores/toggleOpenStore";

// Importing UI components
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Trash2 } from "lucide-vue-next";

/**----------------------------- Methods ----------------------------------- */

// Accessing Pinia stores
const annotationsModalStore = useAnnotationsModalStore();
const { isOpen: isModalOpen } = storeToRefs(annotationsModalStore);

const questionsStore = useQuestionsStore();
// TODO: Fix the way to add comments to the selected answer. Do it locally and then push to the store
const { selectedAnswer, newComment } = storeToRefs(questionsStore);

// TODO: Computed property to check if there are any comments in the selected answer
const hasComments = computed(() => (selectedAnswer.value?.comments?.length ?? 0) > 0);

const closeAnnotationsModal = () => {
  annotationsModalStore.close();
  questionsStore.clearSelectedAnswer();
};

// Methods for managing comments
const addComment = () => {
  questionsStore.addCommentToSelectedAnswer();
};

const deleteComment = (commentIndex: number) => {
  questionsStore.deleteCommentFromSelectedAnswer(commentIndex);
};
</script>

<template>
  <Dialog :open="isModalOpen" @update:open="closeAnnotationsModal">
    <DialogContent class="glassmorphism-modal sm:max-w-[60vh] sm:max-h-[60vh] flex flex-col">
      <!-- Modal Header -->
      <DialogHeader>
        <DialogTitle>Annotations</DialogTitle>
        <DialogDescription class="pb-1 text-gray-300">
          View and add comments for Version {{ selectedAnswer?.configVersion }} of the answer.
        </DialogDescription>
      </DialogHeader>

      <!-- Modal content -->
      <div class="flex-grow flex flex-col overflow-hidden">
        <!-- TODO: Fix the scroll Area height. If it doesn't get a fixed height value, it doesn't show the scrollbar and doesn't scroll at all-->
        <ScrollArea
          :class="[
            'pr-1.5 transition-all duration-300 ease-in-out',
            hasComments ? 'h-[25vh]' : 'h-0'
          ]"
        >
          <div class="space-y-3 p-1">
            <!-- Comment card -->
            <div
              v-for="(comment, index) in selectedAnswer?.comments"
              :key="index"
              class="glassmorphism border-none p-1.5 rounded flex justify-between items-center"
            >
              <p class="text-sm text-gray-50 break-words w-[calc(100%-2.5rem)]">{{ comment }}</p>
              <Button
                name="delete-comment"
                variant="link"
                size="icon"
                class="px-2 text-gray-300 hover:text-red-400 shrink-0"
                @click="deleteComment(index)"
              >
                <Trash2 class="h-4 w-4" />
              </Button>
            </div>
          </div>
        </ScrollArea>

        <Textarea
          v-model="newComment"
          placeholder="Add a new comment..."
          class="mt-3 mb-1 placeholder:text-gray-400"
        />
      </div>

      <!-- Modal footer -->
      <DialogFooter>
        <Button
          variant="ghost"
          class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none"
          @click="closeAnnotationsModal"
          >Close</Button
        >
        <Button
          variant="secondary"
          class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_0%)] border-none"
          @click="addComment"
          >Add Comment</Button
        >
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
