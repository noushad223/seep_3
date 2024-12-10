<script>
    import { goto } from '$app/navigation';
    
    let email = '';
    let password = '';

    const handleSubmit = () => {
        goto('/dashboard');
    };
</script>

<div class="min-h-screen bg-gradient-to-br from-red-50 to-rose-100 py-6 flex flex-col justify-center sm:py-12">
    <div class="relative py-3 sm:max-w-xl sm:mx-auto">
        <div class="absolute inset-0 bg-gradient-to-r from-red-400 to-rose-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
            <div class="max-w-md mx-auto">
                    <h1 class="text-2xl font-semibold text-center mb-8">Login</h1>
                    <form on:submit|preventDefault={handleSubmit} class="py-8 text-base leading-6 space-y-6 text-gray-700 sm:text-lg sm:leading-7">
                        <div class="relative">
                            <input 
                                bind:value={email}
                                type="email" 
                                class="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 placeholder-transparent focus:outline-none focus:border-red-500" 
                                placeholder="Email address"
                                id="email"
                            />
                            <label 
                                for="email" 
                                class="absolute left-0 -top-3.5 text-gray-600 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm"
                            >
                                Email address
                            </label>
                        </div>
                        <div class="relative">
                            <input 
                                bind:value={password}
                                type="password" 
                                class="peer h-10 w-full border-b-2 border-gray-300 text-gray-900 placeholder-transparent focus:outline-none focus:border-red-500" 
                                placeholder="Password"
                                id="password"
                            />
                            <label 
                                for="password" 
                                class="absolute left-0 -top-3.5 text-gray-600 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-2 peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm"
                            >
                                Password
                            </label>
                        </div>
                            <button 
                                type="submit" 
                                class="bg-red-500 text-white rounded-md px-6 py-2 w-full hover:bg-red-600 transition-colors duration-200 transform active:scale-95"
                            >
                                Sign in
                            </button>
                
                    </form>
            </div>
        </div>
    </div>
</div>
