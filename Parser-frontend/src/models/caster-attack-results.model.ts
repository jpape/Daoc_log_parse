export class CasterAttackResults {
    constructor(
        public Crits: number,
        public BaseDamage: number,
        public Landed: number,
        public TotalDamage: number,
        public TotalAttacks: number,
        public Resists: number,
        public CritDamage: number,
        public Targets: string[]
    ) {}
}