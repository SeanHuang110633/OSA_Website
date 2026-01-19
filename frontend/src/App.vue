<template>
  <div class="min-h-screen flex flex-col font-sans">
    <AppHeader />

    <main class="container mx-auto px-6 py-12 flex-grow">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div class="lg:col-span-9 space-y-10">
          <div v-if="!currentEventId">
            <div class="flex items-center space-x-4 mb-6">
              <h2 class="text-2xl text-stone-700 serif-font">最新公告</h2>
              <div class="h-px bg-stone-200 flex-grow"></div>
            </div>

            <div
              v-if="loading"
              class="flex justify-center py-10 text-stone-400"
            >
              <i class="fas fa-spinner fa-spin mr-2"></i> 載入中...
            </div>

            <div v-else class="space-y-4">
              <EventCard
                v-for="event in events"
                :key="event.id"
                :event="event"
                @click="handleEventClick"
              />
            </div>
          </div>

          <div v-else>
            <button
              @click="currentEventId = null"
              class="mb-4 text-sm text-stone-500 hover:text-[#D4A373]"
            >
              <i class="fas fa-arrow-left mr-1"></i> 返回列表
            </button>

            <div v-if="detailLoading" class="text-center py-10">載入中...</div>
            <div v-else-if="eventDetail" class="zen-card p-8">
              <h1 class="text-3xl serif-font text-stone-800 mb-4">
                {{ eventDetail.title }}
              </h1>

              <div
                class="flex gap-4 text-xs text-stone-400 border-b border-stone-100 pb-4 mb-6"
              >
                <span
                  ><i class="far fa-calendar mr-1"></i>
                  {{
                    new Date(eventDetail.published_at).toLocaleDateString()
                  }}</span
                >
                <span
                  ><i class="far fa-folder mr-1"></i>
                  {{ eventDetail.category?.name }}</span
                >
              </div>

              <div
                class="prose max-w-none text-stone-600"
                v-html="eventDetail.content"
              ></div>

              <div
                v-if="eventDetail.attachments?.length"
                class="mt-8 pt-6 border-t border-stone-100"
              >
                <h4 class="text-sm font-bold text-stone-700 mb-3">附件下載</h4>
                <ul class="space-y-2">
                  <li v-for="att in eventDetail.attachments" :key="att.path">
                    <a
                      :href="`http://127.0.0.1:8000${att.path}`"
                      target="_blank"
                      class="flex items-center gap-2 text-sm text-stone-500 hover:text-[#D4A373]"
                    >
                      <i class="fas fa-paperclip"></i> {{ att.title }}
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-3">
          <AppSidebar />
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getEvents, getEventDetail } from "./api/event";

// 引入組件
import AppHeader from "./components/layout/AppHeader.vue";
import AppFooter from "./components/layout/AppFooter.vue";
import AppSidebar from "./components/layout/AppSidebar.vue";
import EventCard from "./components/event/EventCard.vue";

// 狀態
const events = ref([]);
const loading = ref(false);

// 詳情頁狀態 (模擬路由)
const currentEventId = ref(null);
const eventDetail = ref(null);
const detailLoading = ref(false);

// 載入列表
const fetchEvents = async () => {
  loading.value = true;
  try {
    const data = await getEvents({ page: 1, size: 10, locale: "zh-TW" });
    events.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// 處理點擊 (進入詳情)
const handleEventClick = async (id) => {
  currentEventId.value = id;
  detailLoading.value = true;
  try {
    const data = await getEventDetail(id, "zh-TW");
    eventDetail.value = data;
  } catch (err) {
    console.error(err);
  } finally {
    detailLoading.value = false;
  }
};

onMounted(() => {
  fetchEvents();
});
</script>
