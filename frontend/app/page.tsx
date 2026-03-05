// frontend/app/page.tsx


import { getHome } from "@/features/home/api";
import HomeClient from "@/features/home/ui/HomeClient";

export default async function HomePage() {
  const data = await getHome();

  return <HomeClient initialData={data} />;
}