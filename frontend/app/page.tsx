// frontend/app/page.tsx


// import WeatherCard from "@/features/home/ui/WeatherCard";
// import WeatherRow from "@/features/home/ui/WeatherRow";
import { getHome } from "@/features/home/api";
import HomeClient from "@/features/home/ui/HomeClient";

export default async function HomePage() {
  const data = await getHome();

  // ✅ 변경 포인트:
  // - 기존엔 여기서 WeatherCard/WeatherRow를 직접 렌더링했지만
  // - 이제는 서버에서 받은 data를 HomeClient(클라이언트 컴포넌트)에 넘겨서
  //   "삭제 버튼/2-card 이동" 같은 UI 로직만 클라이언트에서 처리합니다.
  // - getHome()로 날씨 내려받는 방식은 그대로 유지됩니다.
  return <HomeClient initialData={data} />;
}