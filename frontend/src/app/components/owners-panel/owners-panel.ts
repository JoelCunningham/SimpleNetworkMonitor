import { BasePanel } from '#components/base/base-panel';
import { AddOwnerCard } from '#components/owners-panel/add-owner-card';
import { OwnerCard } from '#components/owners-panel/owner-card';
import { Owner } from '#interfaces/owner';
import { OwnerService } from '#services/owner-service';
import { ChangeDetectorRef, Component } from '@angular/core';
import { OwnerModal } from './owner-modal';

@Component({
  standalone: true,
  selector: 'app-owners-panel',
  imports: [BasePanel, OwnerCard, AddOwnerCard, OwnerModal],
  templateUrl: './owners-panel.html',
  styleUrl: './owners-panel.scss',
})
export class OwnersPanel {
  protected owners: Owner[] = [];
  protected currentOwner: Owner | null = null;

  protected showOwnerModal = false;

  constructor(
    private ownerService: OwnerService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.ownerService.currentOwners().subscribe((data) => {
      this.owners = data.sort((a, b) => {
        const deviceDiff = (b.devices.length || 0) - (a.devices.length || 0);
        if (deviceDiff !== 0) return deviceDiff;
        return (a.name || '').localeCompare(b.name || '');
      });
      this.cdr.detectChanges();
    });
  }

  openViewModal(owner: Owner) {
    this.currentOwner = owner;
    this.showOwnerModal = true;
  }

  openAddModal() {
    this.currentOwner = { id: 0, name: '', devices: [] };
    this.showOwnerModal = true;
  }

  handleModalClose() {
    this.showOwnerModal = false;
  }

  handleOwnerUpdate(owner: Owner) {
    const ownerIndex = this.owners.findIndex((o) => o.id === owner.id);
    if (ownerIndex !== -1) {
      this.owners[ownerIndex] = owner;
    } else {
      this.owners.push(owner);
    }
  }

  handleOwnerDelete(owner: Owner) {
    this.owners = this.owners.filter((o) => o.id !== owner.id);
    this.currentOwner = null;
    this.showOwnerModal = false;
  }
}
