import { CashResults } from "./cash-results.model";
import { CombatResults } from "./combat-results.model";
import { HealingResults } from "./healing-results.model";

export class ParsingResults {
    constructor(
        public Cash: CashResults,
        public Combat: CombatResults,
        public Healing: HealingResults
    ) { }
}