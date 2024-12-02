<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { derived } from 'svelte/store';

    const coursework = derived(page, ($page) => ({
        id: $page.params.courseworkId,
        moduleId: $page.params.moduleId,
        moduleName: "Software Engineering",
        content: "/EDR.pdf",
        marks: {
            teacher: 85,
            auto: 52
        },
        status: "Needs Review",
        feedback: "This is a hardcoded example of English coursework feedback. Make sure to focus on improving the structure and clarity of your arguments."
    }));

    function rejectAutomarker() {
        console.log('Feedback submitted:');
        goto('/dashboard');
    }

    function acceptAutomarker() {
        console.log('Marked as reviewed');
        goto('/dashboard');
    }

    const discrepancy = derived(coursework, ($coursework) => {
        if (!$coursework.marks.teacher || !$coursework.marks.auto) return 0;
        return Math.abs($coursework.marks.teacher - $coursework.marks.auto);
    });
</script>

<div class="min-h-screen bg-gray-50">
    <div class="fixed top-0 left-0 right-0 bg-white shadow-sm z-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center">
            <a href="/dashboard" class="text-slate-600 hover:text-slate-900" aria-label="Back to Dashboard">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
            </a>
            <h1 class="text-2xl font-bold text-gray-900 flex-1 text-center">
                Coursework {$coursework.id} - {$coursework.moduleName}
            </h1>
            <div class="w-6"></div>
        </div>
    </div>

    <div class="pt-16 flex h-[calc(100vh-4rem)]">
        <div class="w-1/2 p-4 bg-gray-100">
            <iframe
                title="Coursework PDF"
                src={$coursework.content}
                class="w-full h-full border-0 rounded-lg shadow-lg"
            ></iframe>
        </div>

        <div class="w-1/2 p-6 overflow-y-auto">
            <div class="space-y-6">
                <div class="bg-white rounded-lg p-6 shadow-sm">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Marks</h2>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <div class="text-sm text-gray-500">Teacher Mark</div>
                            <div class="text-2xl font-bold text-gray-900">{$coursework.marks.teacher ?? '-'}</div>
                        </div>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <div class="text-sm text-gray-500">Auto Mark</div>
                            <div class="text-2xl font-bold text-gray-900">{$coursework.marks.auto ?? '-'}</div>
                        </div>
                    </div>
                    {#if $discrepancy > 10}
                        <div class="mt-4 p-4 bg-red-50 rounded-md">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                    </svg>
                                </div>
                                <div class="ml-3">
                                    <h3 class="text-sm font-medium text-red-800">Marking Discrepancy Detected</h3>
                                    <div class="mt-2 text-sm text-red-700">
                                        There is a {$discrepancy} point difference between teacher and auto marks.
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/if}
                </div>

                <div class="bg-white rounded-lg p-6 shadow-sm">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Feedback</h2>
                    <div class="space-y-4">
                        <p class="text-gray-700">
                            {$coursework.feedback}
                        </p>
                        <div class="flex justify-end space-x-4">
                            <button
                                on:click={() => acceptAutomarker()}
                                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                            >
                                Accept Automarker
                            </button>
                            <button
                                on:click={() => rejectAutomarker()}
                                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:text-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            >
                                Deny Automarker
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
