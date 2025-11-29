import { ViewDevicesGrid } from '#components/grids';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewDevicesGrid', () => {
  let component: ViewDevicesGrid;
  let fixture: ComponentFixture<ViewDevicesGrid>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewDevicesGrid],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewDevicesGrid);
    component = fixture.componentInstance;

    // Set required input
    component.owner = { id: 1, name: 'Test Owner', devices: [] };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
