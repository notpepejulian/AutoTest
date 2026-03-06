import type { APIRoute } from 'astro';

export const prerender = false;

const BACKEND_URL = (import.meta as any).env.BACKEND_API_URL || 'http://backend:8000/api';

export const ALL: APIRoute = async ({ request, params, cookies }) => {
    const { path } = params;
    const url = new URL(request.url);
    const searchParams = url.searchParams.toString();

    const backendUrl = `${BACKEND_URL}/${path}${searchParams ? '?' + searchParams : ''}`;

    console.log(`Proxying request: ${request.method} ${request.url} -> ${backendUrl}`);

    try {
        // For POST requests with FormData (like login), we need to handle it carefully
        let fetchOptions: RequestInit = {
            method: request.method,
            headers: {
                ...Object.fromEntries(request.headers.entries()),
            }
        };

        // Remove headers that might conflict or be incorrect after transformation
        delete (fetchOptions.headers as any)['host'];
        delete (fetchOptions.headers as any)['content-length'];
        delete (fetchOptions.headers as any)['connection'];

        if (request.method !== 'GET' && request.method !== 'HEAD') {
            const contentType = request.headers.get('content-type');

            if (path === 'auth/login') {
                // Special handling for OAuth2 login (expects x-www-form-urlencoded)
                const formData = await request.formData();
                const searchParams = new URLSearchParams();
                for (const [key, value] of formData.entries()) {
                    searchParams.append(key, value.toString());
                }

                // Override headers for this specific call to be safe
                fetchOptions.headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                };
                fetchOptions.body = searchParams.toString();
                console.log(`Login payload sent: ${fetchOptions.body}`);
            } else if (contentType?.includes('application/json')) {
                fetchOptions.body = JSON.stringify(await request.json());
            } else if (contentType?.includes('multipart/form-data') || contentType?.includes('application/x-www-form-urlencoded')) {
                const formData = await request.formData();
                fetchOptions.body = formData;
                // Let fetch set the boundary for multipart/form-data
                if (contentType?.includes('multipart/form-data')) {
                    delete (fetchOptions.headers as any)['content-type'];
                }
            } else {
                fetchOptions.body = await request.arrayBuffer();
            }
        }

        const response = await fetch(backendUrl, fetchOptions);

        // Special logic for Auth
        if (path === 'auth/login' && response.ok) {
            const data = await response.json();

            // Set the session cookie
            cookies.set('access_token', data.access_token, {
                path: '/',
                httpOnly: true,
                secure: (import.meta as any).env.PROD,
                sameSite: 'strict',
                maxAge: 60 * 60 * 24, // 24 hours
            });

            return new Response(JSON.stringify({ user: data.user }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        if (path === 'auth/logout') {
            cookies.delete('access_token', { path: '/' });
            return new Response(JSON.stringify({ message: 'Sesión cerrada' }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        // Default: Return the backend response
        return new Response(response.body, {
            status: response.status,
            headers: response.headers,
        });
    } catch (error) {
        console.error(`Proxy error for ${backendUrl}:`, error);
        return new Response(JSON.stringify({ detail: 'Error al conectar con el servidor backend' }), {
            status: 502,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};
