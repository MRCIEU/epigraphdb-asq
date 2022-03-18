import store from "@/store/index.ts";

export function checkStageComplete(stage: number): boolean {
  // @ts-ignore
  const latestStage: number = store.state.queryStage.latestStage;
  const res = latestStage > stage;
  return res;
}

export function formatUrl(ent_id: string, meta_ent: string): string {
  const res = `https://epigraphdb.org/entity?meta_node=${meta_ent}&id=${ent_id}`;
  return res;
}

export function refEntValid(ent_id: string | null): boolean {
  const fakeIds = ["query-triple-subj", "query-triple-obj"];
  if (ent_id == null) {
    return false;
  } else if (fakeIds.includes(ent_id)) {
    return false;
  }
  return true;
}
