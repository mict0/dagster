/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { BulkActionStatus, BackfillStatus, RunStatus } from "./../../types/globalTypes";

// ====================================================
// GraphQL query operation: InstanceBackfillsQueryNew
// ====================================================

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_partitionRunStats {
  __typename: "BackfillRunStats";
  numQueued: number;
  numInProgress: number;
  numSucceeded: number;
  numFailed: number;
  numPartitionsWithRuns: number;
  numTotalRuns: number;
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_unfinishedRuns {
  __typename: "Run";
  id: string;
  canTerminate: boolean;
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_partitionSet_repositoryOrigin {
  __typename: "RepositoryOrigin";
  id: string;
  repositoryName: string;
  repositoryLocationName: string;
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_partitionSet {
  __typename: "PartitionSet";
  id: string;
  name: string;
  mode: string;
  pipelineName: string;
  repositoryOrigin: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_partitionSet_repositoryOrigin;
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_error_cause {
  __typename: "PythonError";
  message: string;
  stack: string[];
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_error {
  __typename: "PythonError";
  message: string;
  stack: string[];
  cause: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_error_cause | null;
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_runs_tags {
  __typename: "PipelineTag";
  key: string;
  value: string;
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_runs {
  __typename: "Run";
  id: string;
  canTerminate: boolean;
  status: RunStatus;
  tags: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_runs_tags[];
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results {
  __typename: "PartitionBackfill";
  backfillId: string;
  status: BulkActionStatus;
  backfillStatus: BackfillStatus;
  numRequested: number;
  partitionNames: string[];
  numPartitions: number;
  partitionRunStats: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_partitionRunStats;
  unfinishedRuns: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_unfinishedRuns[];
  timestamp: number;
  partitionSetName: string;
  partitionSet: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_partitionSet | null;
  error: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_error | null;
  runs: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results_runs[];
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills {
  __typename: "PartitionBackfills";
  results: InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills_results[];
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PythonError_cause {
  __typename: "PythonError";
  message: string;
  stack: string[];
}

export interface InstanceBackfillsQueryNew_partitionBackfillsOrError_PythonError {
  __typename: "PythonError";
  message: string;
  stack: string[];
  cause: InstanceBackfillsQueryNew_partitionBackfillsOrError_PythonError_cause | null;
}

export type InstanceBackfillsQueryNew_partitionBackfillsOrError = InstanceBackfillsQueryNew_partitionBackfillsOrError_PartitionBackfills | InstanceBackfillsQueryNew_partitionBackfillsOrError_PythonError;

export interface InstanceBackfillsQueryNew {
  partitionBackfillsOrError: InstanceBackfillsQueryNew_partitionBackfillsOrError;
}

export interface InstanceBackfillsQueryNewVariables {
  cursor?: string | null;
  limit?: number | null;
}
