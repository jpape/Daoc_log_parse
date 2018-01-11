import { DefenseResults } from './defense-results.model';
import { CasterAttackResults } from './caster-attack-results.model';
import { MeleeAttackResults } from './melee-attack-results.model';

export class CombatResults {
    constructor(
        public Defense: DefenseResults,
        public CasterAttack: CasterAttackResults,
        public MeleeAttack: MeleeAttackResults
    ) {}
}