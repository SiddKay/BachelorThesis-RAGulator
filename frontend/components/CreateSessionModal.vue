<script setup lang="ts">
import { ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import type { SessionCreate } from "@/types/api";
import { useSessionStore } from "@/stores/sessions.store";
import { useCreateSessionModalStore } from "@/stores/toggleOpen.store";

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
import { Textarea } from "@/components/ui/textarea";

const router = useRouter();
const sessionModalStore = useCreateSessionModalStore();
const { isOpen: isModalOpen } = storeToRefs(sessionModalStore);

const sessionStore = useSessionStore();
const { isLoading } = storeToRefs(sessionStore);

const newSession = ref<SessionCreate>({
  name: "",
  description: ""
});

const error = ref<string | null>(null);

const saveNewSession = async () => {
  if (!newSession.value.name.trim()) {
    error.value = "Session name is required.";
    return;
  }

  try {
    await sessionStore.createSession(newSession.value);
    if (sessionStore.currentSession?.id) {
      router.push(`/sessions/${sessionStore.currentSession.id}/evaluation`);
    }
    resetModal();
  } catch (err) {
    error.value = `Failed to create session: ${err instanceof Error ? err.message : "Unknown error"}`;
  }
};

const resetModal = () => {
  sessionModalStore.close();
  newSession.value = {
    name: "",
    description: ""
  };
  error.value = null;
};

watch(isModalOpen, (isOpen) => {
  if (!isOpen) resetModal();
});
</script>

<template>
  <Dialog :open="isModalOpen" @update:open="sessionModalStore.close">
    <DialogContent class="glassmorphism-modal sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Create New Session</DialogTitle>
        <DialogDescription class="text-gray-300">
          Create a new evaluation session for your RAG pipeline.
        </DialogDescription>
      </DialogHeader>

      <div v-if="error" class="text-red-400 text-sm mb-2">
        {{ error }}
      </div>

      <div class="space-y-4">
        <div class="space-y-2">
          <label for="name" class="text-sm text-gray-300">Session Name</label>
          <Input
            id="name"
            v-model="newSession.name"
            placeholder="Enter session name"
            class="placeholder:text-gray-400"
            :disabled="isLoading"
          />
        </div>

        <div class="space-y-2">
          <label for="description" class="text-sm text-gray-300">Description (Optional)</label>
          <Textarea
            id="description"
            v-model="newSession.description"
            placeholder="Enter session description"
            class="placeholder:text-gray-400 max-h-[180px]"
            :disabled="isLoading"
          />
        </div>
      </div>

      <DialogFooter>
        <div class="flex space-x-2">
          <Button
            variant="ghost"
            class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_10%)] hover:glassmorphism hover:border-none select-none touch-none"
            :disabled="isLoading"
            @click="resetModal"
          >
            Cancel
          </Button>
          <Button
            variant="secondary"
            class="[text-shadow:_0_1px_1px_rgb(0_0_0_/_0%)] border-none select-none touch-none"
            :disabled="isLoading"
            @click="saveNewSession"
          >
            Create
          </Button>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
