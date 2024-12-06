<script setup lang="ts">
import { ref } from "vue";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Pencil, Check, Trash2 } from "lucide-vue-next";

import { useSessionStore } from "@/stores/sessions.store";
import type { Session } from "@/types/api";
import { formatDate } from "@/lib/utils";

const sessionsStore = useSessionStore();
const props = defineProps<{ session: Session }>();
const isEditing = ref(false);
const editedSessionName = ref(props.session.name);

const handleDelete = async () => {
  if (confirm("Are you sure you want to delete this session?")) {
    await sessionsStore.deleteSession(props.session.id);
  }
};

const handleEdit = async () => {
  if (isEditing.value) {
    // Save the edited session name
    await sessionsStore.updateSession(props.session.id, {
      name: editedSessionName.value
    });
    isEditing.value = false;
  } else {
    // Enter edit mode
    isEditing.value = true;
  }
};
</script>

<template>
  <Card class="w-full p-1 glassmorphism">
    <CardHeader class="p-3 pb-2">
      <!-- Session -->
      <CardTitle class="flex items-center justify-between gap-2">
        <div class="flex-grow">
          <Input
            v-if="isEditing"
            v-model="editedSessionName"
            class="max-w-full"
            :placeholder="props.session.name"
            @click.stop.prevent
          />
          <span v-else class="text-md font-semibold">{{ props.session.name }}</span>
        </div>
        <div class="flex gap-2">
          <Button
            size="xs"
            variant="ghost"
            class="text-blue-400 hover:glassmorphism hover:border-none transition-colors"
            aria-label="Edit"
            :title="isEditing ? 'Save' : 'Edit'"
            @click.stop.prevent="handleEdit"
          >
            <component :is="isEditing ? Check : Pencil" class="h-4 w-4"
          /></Button>
          <Button
            size="xs"
            variant="ghost"
            class="text-red-400 hover:glassmorphism hover:border-none transition-colors"
            aria-label="Delete"
            title="Delete"
            @click.stop.prevent="handleDelete"
          >
            <Trash2 class="h-4 w-4" />
          </Button>
        </div>
      </CardTitle>
    </CardHeader>

    <CardContent class="p-3 pt-1">
      <div class="flex justify-between items-start gap-20">
        <p class="text-sm text-gray-300 flex-1 break-words">
          {{ props.session.description }}
        </p>
        <div class="text-xs text-gray-400 flex flex-col items-end shrink-1">
          <div class="flex gap-2">
            <span>Created:</span>
            <span> {{ formatDate(props.session.created_at.toLocaleString()) }}</span>
          </div>
          <div class="flex gap-2 shrink-1">
            <span>Last Modified:</span>
            <span>{{ formatDate(props.session.last_modified.toLocaleString()) }}</span>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
