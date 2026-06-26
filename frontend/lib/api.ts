const LOCAL_API_URL = "http://localhost:8000";

export function getApiBaseUrl() {
  const configuredUrl = process.env.NEXT_PUBLIC_API_URL?.trim().replace(
    /\/$/,
    "",
  );

  if (configuredUrl) {
    return configuredUrl;
  }

  if (typeof window !== "undefined") {
    const { hostname, origin } = window.location;

    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return LOCAL_API_URL;
    }

    return origin;
  }

  return LOCAL_API_URL;
}
