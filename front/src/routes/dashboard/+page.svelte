<script lang="ts">
    import { derived, writable } from 'svelte/store';

    const modules = writable([
        {
            id: 1,
            name: "Software Engineering",
            courseworks: [
                { id: "CW1", status: "Needs Review", marks: { teacher: 75, auto: 85 } },
                { id: "CW2", status: "Checked", marks: { teacher: 88, auto: 90 } }
            ]
        },
        {
            id: 2,
            name: "Database Systems",
            courseworks: [
                { id: "CW1", status: "Unchecked", marks: { teacher: null, auto: 78 } }
            ]
        }
    ]);

    const searchQuery = writable('');

    const filteredModules = derived([modules, searchQuery], ([$modules, $searchQuery]) =>
        $modules.filter((module) =>
            module.name.toLowerCase().includes($searchQuery.toLowerCase())
        )
    );

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'Needs Review':
                return 'text-yellow-600 bg-yellow-100';
            case 'Checked':
                return 'text-green-600 bg-green-100';
            case 'Unchecked':
                return 'text-gray-600 bg-gray-100';
            default:
                return 'text-gray-600 bg-gray-100';
        }
    };

    const hasMarkingDiscrepancy = (marks: { teacher: number | null; auto: number | null }) => {
        if (!marks.teacher || !marks.auto) return false;
        return Math.abs(marks.teacher - marks.auto) > 10;
    };
</script>

<div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
            <div class="mt-4">
                <div class="relative">
                    <input
                        type="text"
                        bind:value={$searchQuery}
                        placeholder="Search modules..."
                        class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-red-500 focus:border-red-500"
                    />
                    <svg
                        class="absolute right-3 top-2.5 h-5 w-5 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                    </svg>
                </div>
            </div>
        </div>

        <div class="bg-white rounded-lg shadow">
            <div class="divide-y divide-gray-200">
                {#each $filteredModules as module}
                    <div class="p-6">
                        <h2 class="text-xl font-semibold text-gray-900 mb-4">{module.name}</h2>
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Coursework
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Status
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Teacher Mark
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Auto Mark
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    {#each module.courseworks as coursework}
                                        <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                {coursework.id}
                                                {#if hasMarkingDiscrepancy(coursework.marks)}
                                                    <span
                                                        class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800"
                                                    >
                                                        Discrepancy
                                                    </span>
                                                {/if}
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm">
                                                <span
                                                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {getStatusColor(coursework.status)}"
                                                >
                                                    {coursework.status}
                                                </span>
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {coursework.marks.teacher ?? '-'}
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {coursework.marks.auto ?? '-'}
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                <a
                                                    href="/coursework/{module.id}/{coursework.id}"
                                                    class="text-red-600 hover:text-red-900"
                                                >
                                                    View Details
                                                </a>
                                            </td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>
