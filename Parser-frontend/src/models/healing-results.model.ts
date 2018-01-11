export class HealingResults {
    constructor(
        public Delivered: number,
        public Lifetapped: number,
        public Received: number,
        public Sources: string[],      
        public Targets: string[]
    ) {}
}