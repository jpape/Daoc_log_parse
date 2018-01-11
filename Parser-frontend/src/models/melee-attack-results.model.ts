export class MeleeAttackResults {
    constructor(
        public Crits: number,
        public Blocks: number,
        public Hits: number,
        public BaseDamage: number,
        public Evades: number,
        public Parries: number,
        public TotalDamage: number,
        public TotalAttacks: number,
        public Misses: number,
        public CritDamage: number,
        public Targets: string[]
    ) {}
}